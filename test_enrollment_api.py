#!/usr/bin/env python3
"""
Test the enrollment API endpoint
"""
import requests
import json


def test_enrollment_api():
    """Test the enrollment form API endpoint"""
    print("🧪 Testing Enrollment API Endpoint...\n")
    
    # Test data
    test_enrollment = {
        "name": "Test Student",
        "email": "test@example.com",
        "phone": "+91 9876543210",
        "city": "Mumbai",
        "course_title": "Stock Market Fundamentals",
        "course_price": "₹15,000"
    }
    
    try:
        # Make API call
        response = requests.post(
            "http://localhost:8000/api/v1/enrollments/form",
            json=test_enrollment,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Enrollment API is working!")
            print(f"📝 Response: {result.get('message', 'Success')}")
            print(f"🆔 Enrollment ID: {result.get('enrollment_id', 'N/A')}")
            print(f"👤 User Created: {result.get('user_created', False)}")
        else:
            print("❌ API Error:")
            try:
                error = response.json()
                print(f"   Error Details: {error.get('detail', 'Unknown error')}")
            except:
                print(f"   HTTP Error: {response.status_code}")
                print(f"   Response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Backend server is not running")
        print("   Please start the backend server with:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        
    except Exception as e:
        print(f"❌ Test Error: {e}")


if __name__ == "__main__":
    test_enrollment_api()