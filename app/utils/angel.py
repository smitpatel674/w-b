from typing import List, Dict, Optional, Tuple
import time
import json

# Support both package names (smartapi-python published under different names)
try:
    # Most common (smartapi-python)
    from smartapi import SmartConnect  # type: ignore
except Exception:  # pragma: no cover
    from SmartApi import SmartConnect  # type: ignore

from app.core.config import settings

def _extract_token(row: dict) -> str:
    # Handle different SDK field casings
    for key in ("symboltoken", "symbolToken", "token", "symbol_token"):
        val = row.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()
    return ""

def _extract_tsym(row: dict) -> str:
    for key in ("tradingsymbol", "tradingSymbol", "tsym", "symbol", "name"):
        val = row.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()
    return ""

ResolvedToken = Tuple[str, str]  # (symboltoken, resolved_tradingsymbol)

class AngelService:
    def __init__(self) -> None:
        self.api_key = settings.angel_api_key
        self.client_id = settings.angel_client_id
        self.refresh_token = settings.angel_refresh_token
        self.feed_token = settings.angel_feed_token
        self.totp_secret = settings.angel_totp_secret
        self.password = settings.angel_password
        self.mpin = settings.angel_mpin
        self._conn: Optional[SmartConnect] = None
        self._last_login_ts: float = 0.0
        self._instrument_cache: dict[str, list[dict]] = {}
        self._token_cache: dict[tuple[str, str], ResolvedToken] = {}
        self._price_cache: dict[tuple[str, str], float] = {}
        self.last_error: Optional[str] = None
        self.debug_tokens: dict[str, Optional[str]] = {}
        self.session_method: Optional[str] = None

    def _login_with_refresh(self, conn: SmartConnect) -> bool:
        if hasattr(conn, 'generateSessionByRefreshToken') and self.refresh_token:
            try:
                conn.generateSessionByRefreshToken(self.refresh_token)  # type: ignore
                self.session_method = 'generateSessionByRefreshToken(refresh_token)'
                return True
            except Exception:
                pass
        if hasattr(conn, 'generateSessionBySessionToken') and self.refresh_token:
            try:
                conn.generateSessionBySessionToken(self.refresh_token)  # type: ignore
                self.session_method = 'generateSessionBySessionToken(refresh_token)'
                return True
            except Exception:
                pass
        if hasattr(conn, 'refreshAccessToken') and self.refresh_token:
            try:
                conn.refreshAccessToken(self.refresh_token)  # type: ignore
                self.session_method = 'refreshAccessToken(refresh_token)'
                return True
            except Exception:
                pass
        return False

    def _login_with_totp_password(self, conn: SmartConnect) -> bool:
        try:
            import pyotp
        except Exception:
            return False
        if not (self.client_id and self.password and self.totp_secret):
            return False
        if not hasattr(conn, 'generateSession'):
            return False
        try:
            otp = pyotp.TOTP(self.totp_secret).now()
            conn.generateSession(self.client_id, self.password, otp)  # type: ignore
            self.session_method = 'generateSession(client_id, password, otp)'
            return True
        except Exception:
            # e.g., AB7001 LoginbyPassword not allowed → fall back to MPIN
            return False

    def _login_with_mpin(self, conn: SmartConnect) -> bool:
        try:
            import pyotp
        except Exception:
            return False
        if not (self.client_id and self.mpin and self.totp_secret):
            return False
        if not hasattr(conn, 'generateSession'):
            return False
        try:
            otp = pyotp.TOTP(self.totp_secret).now()
            conn.generateSession(self.client_id, self.mpin, otp)  # type: ignore
            self.session_method = 'generateSession(client_id, mpin, otp)'
            return True
        except Exception:
            return False

    def _ensure_session(self) -> SmartConnect:
        try:
            if self._conn is not None and (time.time() - self._last_login_ts) < 60 * 30:
                return self._conn
            if not self.api_key:
                raise RuntimeError("Angel API key missing")
            conn = SmartConnect(api_key=self.api_key)

            if self._login_with_refresh(conn) or self._login_with_totp_password(conn) or self._login_with_mpin(conn):
                self._conn = conn
                self._last_login_ts = time.time()
                self.last_error = None
                return conn
            raise RuntimeError("No supported login method succeeded. Provide valid refresh token or password+TOTP or mpin+TOTP.")
        except Exception as e:
            self.last_error = f"session_error: {e}"
            raise

    def _load_instruments(self, exchange: str) -> list[dict]:
        # Not all SDKs expose getInstruments; guard it
        if exchange in self._instrument_cache and self._instrument_cache[exchange]:
            return self._instrument_cache[exchange]
        conn = self._ensure_session()
        if hasattr(conn, 'getInstruments'):
            try:
                data = conn.getInstruments(exchange)  # type: ignore
                self._instrument_cache[exchange] = data or []
                self.last_error = None
                # Debug: Log first few instruments to see format
                if self._instrument_cache[exchange]:
                    print(f"DEBUG: First 3 {exchange} instruments:")
                    for i, inst in enumerate(self._instrument_cache[exchange][:3]):
                        print(f"  {i}: {inst}")
                return self._instrument_cache[exchange]
            except Exception as e:
                self.last_error = f"getInstruments_error: {e}"
        # Fallback: fetch public scrip master JSON directly from Angel One
        try:
            import httpx  # lazy import
            url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
            resp = httpx.get(url, timeout=10.0)
            resp.raise_for_status()
            data = resp.json()
            # Filter by exchange, normalize keys
            results: list[dict] = []
            for row in data:
                exch = str(row.get('exch_seg', '')).upper()
                if exch.startswith('NSE') and exchange.upper().startswith('NSE'):
                    results.append(row)
                elif exch.startswith('BSE') and exchange.upper().startswith('BSE'):
                    results.append(row)
            self._instrument_cache[exchange] = results
            if results:
                print(f"DEBUG: Loaded {len(results)} instruments from public JSON for {exchange}")
            return self._instrument_cache[exchange]
        except Exception as e:
            print(f"DEBUG: public instruments load failed: {e}")
        # If not available or failed, keep cache empty and rely on searchScrip
        self._instrument_cache[exchange] = []
        return []

    def _search_token(self, exchange: str, tradingsymbol: str) -> Optional[ResolvedToken]:
        conn = self._ensure_session()
        if not hasattr(conn, 'searchScrip'):
            return None
        try:
            # Try different exchange aliases some SDKs expect
            exchange_aliases = [exchange, 'NSE', 'NSE_EQ', 'NSECM']

            # Try different search terms
            search_terms = [
                tradingsymbol,
                tradingsymbol.replace("-EQ", ""),
                tradingsymbol.replace("_", ""),
                tradingsymbol.upper(),
                tradingsymbol.lower()
            ]

            for exch in exchange_aliases:
                for search_term in search_terms:
                    payload = {"exchange": exch, "search": search_term}
                    res = conn.searchScrip(payload)  # type: ignore
                    data = res.get('data', []) if isinstance(res, dict) else []

                    # Debug first few results
                    if data:
                        print(f"DEBUG searchScrip exch={exch} term={search_term} count={len(data)}")

                    candidates = [tradingsymbol, f"{tradingsymbol}-EQ", search_term]
                    for row in data:
                        tsym = _extract_tsym(row)
                        name = str(row.get('name', '')).strip()
                        symbol = str(row.get('symbol', '')).strip()

                        # Strict matching to avoid symbol confusion
                        if tsym in candidates or name in candidates or symbol in candidates:
                            token = _extract_token(row)
                            if token and token != '0':
                                return (token, tsym)
            return None
        except Exception as e:
            self.last_error = f"searchScrip_error: {e}"
            return None

    def _resolve_token(self, exchange: str, tradingsymbol: str) -> Optional[ResolvedToken]:
        key = (exchange, tradingsymbol)
        if key in self._token_cache:
            return self._token_cache[key]
        instruments = self._load_instruments(exchange)
        resolved: Optional[ResolvedToken] = None
        if instruments:
            # Try multiple variations of the symbol
            candidates = [
                tradingsymbol,
                f"{tradingsymbol}-EQ", 
                f"{tradingsymbol}",
                tradingsymbol.replace("-EQ", ""),
                tradingsymbol.replace("_", ""),
                tradingsymbol.upper(),
                tradingsymbol.lower()
            ]
            
            for row in instruments:
                tsym = _extract_tsym(row)
                name = str(row.get('name', '')).strip()
                symbol = str(row.get('symbol', '')).strip()
                
                # Check if any candidate provides an exact match to avoid symbol confusion
                if tsym in candidates or name in candidates or symbol in candidates:
                    tok = _extract_token(row)
                    if tok and tok != '0':
                        resolved = (tok, tsym)
                        break
        # If not found via instrument dump, try searchScrip
        if not resolved:
            resolved = self._search_token(exchange, tradingsymbol)
        
        if resolved:
            print(f"DEBUG: Resolved {tradingsymbol} to token {resolved[0]} ({resolved[1]})")
        else:
            print(f"DEBUG: Failed to resolve token for {tradingsymbol}")

        self.debug_tokens[tradingsymbol] = resolved[0] if resolved else None
        if resolved:
            self._token_cache[key] = resolved
            self.last_error = None
        else:
            self.last_error = f"token_not_found: {exchange}:{tradingsymbol}"
        return resolved

    def get_ltp(self, exchange: str, tradingsymbol: str) -> float:
        cache_key = (exchange, tradingsymbol)
        last_good = self._price_cache.get(cache_key, 0.0)
        for attempt in range(3):
            try:
                conn = self._ensure_session()
                resolved = self._resolve_token(exchange, tradingsymbol)
                if not resolved:
                    return last_good
                token, resolved_tsym = resolved
                data = conn.ltpData(exchange=exchange, tradingsymbol=resolved_tsym, symboltoken=token)
                print(f"DEBUG: ltpData for {resolved_tsym} response: {data}")
                price = float(data.get('data', {}).get('ltp', 0.0))
                if price > 0:
                    self._price_cache[cache_key] = price
                self.last_error = None
                return price if price > 0 else last_good
            except Exception as e:
                self.last_error = f"ltp_error_attempt_{attempt+1}: {e}"
                # Force re-login on session issues
                if 'TokenExpired' in str(e) or 'session' in str(e).lower():
                    self._conn = None
                # Backoff: 0.5s, 1.0s, 1.5s
                time.sleep(0.5 * (attempt + 1))
        # All retries failed; return last known good price if any
        return last_good

    def get_many_ltp(self, items: List[Dict[str, str]]) -> List[Dict[str, float]]:
        out: List[Dict[str, float]] = []
        for it in items:
            exch = it.get('exchange', 'NSE')
            sym = it.get('tradingsymbol', '')
            price = self.get_ltp(exch, sym)
            out.append({ 'symbol': sym if sym else '', 'price': price })
        return out

angel_service = AngelService()
