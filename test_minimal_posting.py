#!/usr/bin/env python3
"""
Minimal LinkedIn posting test - trying to find what works with our token
"""

import requests
import json
import sys

# Current access token
ACCESS_TOKEN = "AQXc2wAcVEPegPIP-wbRWEqqgCVB5lQ5tchyB4so2SU6w37ancjCGqaltY1lAHiZYOCvPIWDskeTlyXoo55FdV8sD1a_2qi_Kb_OWMs_oerJxsW0crzqLvMwG0b6YHOl6OeRXY6C1mhykQNO94vuWvYo9WhB_mNjUdqGy5h1cqw2gnx_K2Bo4r-aeRgtTt38u32pDM60byHJKLJaEHGNvBendUTCDzL4BDUkUOCRod31oEclO3QFjfmFZGq2RFzd5wJg0TMsoUt4JL69AgMRuTwuk8LaRdHHF7-O6kMyOg5chQk9ve_pJpBpiQ1nKf_Bd2kTIKtRHuAvTZayeYUoL-VDSlN_pw"

def test_api_endpoints():
    """Test various LinkedIn API endpoints to see what works"""
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    # List of endpoints to test
    endpoints_to_test = [
        # Basic profile endpoints
        ('GET', 'https://api.linkedin.com/v2/people/~', 'Basic profile info'),
        ('GET', 'https://api.linkedin.com/v2/me', 'Current user info'),
        
        # Share endpoints (older API)
        ('GET', 'https://api.linkedin.com/v1/people/~', 'V1 profile'),
        
        # Try different UGC endpoints
        ('GET', 'https://api.linkedin.com/v2/shares', 'List shares'),
        ('GET', 'https://api.linkedin.com/v2/ugcPosts', 'List UGC posts'),
        
        # Check what permissions we have
        ('GET', 'https://api.linkedin.com/v2/oauth/introspect', 'Token introspection'),
    ]
    
    print("🔍 Testing LinkedIn API endpoints with current token...\n")
    
    for method, url, description in endpoints_to_test:
        try:
            print(f"Testing: {description}")
            print(f"  {method} {url}")
            
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, headers=headers, timeout=10)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                data = response.json()
                print(f"  ✅ Success!")
                print(f"  Data: {json.dumps(data, indent=2)[:200]}...")
            elif response.status_code == 403:
                print(f"  ❌ Access denied - insufficient permissions")
                try:
                    error_data = response.json()
                    print(f"  Error: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"  Error: {response.text[:100]}...")
            elif response.status_code == 404:
                print(f"  ❌ Endpoint not found")
            else:
                print(f"  ❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"  Message: {error_data.get('message', 'Unknown error')}")
                except:
                    print(f"  Raw error: {response.text[:100]}...")
            
            print()
            
        except requests.exceptions.Timeout:
            print(f"  ❌ Timeout")
            print()
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request failed: {e}")
            print()
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            print()

def test_simple_post():
    """Try to post using the simplest possible method"""
    
    print("🚀 Attempting simple text post...\n")
    
    # Try the most basic UGC post format
    post_data = {
        "author": "urn:li:person:ACoAAAl75fkBbH8kZ8Q8Z5Q8Z5Q8Z5Q8Z5Q8Z5",  # Placeholder - we need real ID
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "🤖 Hello LinkedIn! This is a test post from my automation bot. #TestPost #Automation"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=post_data,
            timeout=15
        )
        
        print(f"Post attempt status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ Post successful!")
            print(f"Response: {response.json()}")
        else:
            print("❌ Post failed")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Post failed with exception: {e}")

if __name__ == "__main__":
    print("=== LinkedIn API Diagnostics ===\n")
    test_api_endpoints()
    print("\n" + "="*50 + "\n")
    test_simple_post()