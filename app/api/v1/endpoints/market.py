from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import time
from app.utils.angel import angel_service
from app.utils.market_indices import market_indices_service

router = APIRouter()

# Cache for live quotes
cache = {}
CACHE_TTL_SECONDS = 0.5  # Cache for 0.5 seconds

class Quote(BaseModel):
    symbol: str
    price: float
    changePercent: float | None = None

class QuotesResponse(BaseModel):
    quotes: list[Quote]
    ts: int
    total: int

@router.get("/indices", response_model=QuotesResponse)
async def get_market_indices():
    """Get the 4 key Indian market indices: NIFTY 50, Bank NIFTY, Sensex, India VIX"""
    cache_key = "market_indices"
    current_time = time.time()

    if cache_key in cache and current_time - cache[cache_key]["ts"] < CACHE_TTL_SECONDS:
        return cache[cache_key]

    try:
        # Get the 4 key Indian market indices
        indices_data = await market_indices_service.get_market_indices_async()
        quotes = [Quote(symbol=item["symbol"], price=item["price"]) for item in indices_data]
        response = {"quotes": quotes, "ts": int(current_time), "total": len(indices_data)}
        cache[cache_key] = response
        return response
    except Exception as e:
        # Fallback to sample data if real data fails
        fallback_data = market_indices_service._get_fallback_data()
        quotes = [Quote(symbol=item["symbol"], price=item["price"]) for item in fallback_data]
        response = {"quotes": quotes, "ts": int(current_time), "total": len(fallback_data)}
        return response


@router.get("/live", response_model=QuotesResponse)
async def get_live_quotes(limit: int = 10, offset: int = 0):
    """Get live NIFTY 50 stocks data"""
    cache_key = f"nifty50_stocks_{limit}:{offset}"
    current_time = time.time()

    if cache_key in cache and current_time - cache[cache_key]["ts"] < CACHE_TTL_SECONDS:
        return cache[cache_key]

    # NIFTY 50 stocks symbols
    symbols = [
        "RELIANCE-EQ", "TCS-EQ", "HDFCBANK-EQ", "ICICIBANK-EQ", "INFY-EQ",
        "ITC-EQ", "LT-EQ", "SBIN-EQ", "HINDUNILVR-EQ", "BHARTIARTL-EQ",
        "KOTAKBANK-EQ", "AXISBANK-EQ", "BAJFINANCE-EQ", "ADANIENT-EQ", "ADANIPORTS-EQ",
        "ASIANPAINT-EQ", "TITAN-EQ", "ULTRACEMCO-EQ", "MARUTI-EQ", "M&M-EQ",
        "NTPC-EQ", "POWERGRID-EQ", "TATAMOTORS-EQ", "TATASTEEL-EQ", "SUNPHARMA-EQ",
        "WIPRO-EQ", "TECHM-EQ", "HCLTECH-EQ", "NESTLEIND-EQ", "JSWSTEEL-EQ",
        "GRASIM-EQ", "CIPLA-EQ", "DRREDDY-EQ", "BRITANNIA-EQ", "ONGC-EQ",
        "COALINDIA-EQ", "HEROMOTOCO-EQ", "EICHERMOT-EQ", "BAJAJFINSV-EQ", "HDFCLIFE-EQ",
        "SBILIFE-EQ", "DIVISLAB-EQ", "APOLLOHOSP-EQ", "BPCL-EQ", "BAJAJ-AUTO-EQ",
        "TATACONSUM-EQ", "HINDALCO-EQ", "INDUSINDBK-EQ", "TATAPOWER-EQ", "UPL-EQ"
    ]
    
    # Apply pagination
    paginated_symbols = symbols[offset:offset + limit]
    
    instruments = [{"exchange": "NSE", "tradingsymbol": s} for s in paginated_symbols]
    try:
        ltps = angel_service.get_many_ltp(instruments)
        quotes = [Quote(symbol=it["symbol"], price=it["price"]) for it in ltps]
        response = {"quotes": quotes, "ts": int(current_time), "total": len(symbols)}
        cache[cache_key] = response
        return response
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"NIFTY 50 stocks fetch failed: {e}")

@router.get("/health")
async def market_health():
    # Try making a lightweight call: load instruments for NSE and resolve a token
    status: dict = {
        "session_ok": False,
        "last_error": angel_service.last_error,
        "resolved_tokens": angel_service.debug_tokens,
    }
    try:
        # Ensure session
        _ = angel_service._ensure_session()
        status["session_ok"] = True
        # Try resolve a token
        _ = angel_service._resolve_token("NSE", "RELIANCE")
        return status
    except Exception as e:
        status["session_ok"] = False
        status["error"] = str(e)
        return status
