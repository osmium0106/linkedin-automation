#!/usr/bin/env python3
"""
Test API-Based LinkedIn Bot
Test the API functionality locally before GitHub Actions
"""

import os
from datetime import datetime

def test_environment():
    """Test environment variables"""
    print("🔐 Testing Environment Variables")
    print("=" * 35)
    
    required_vars = ['LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET']
    optional_vars = ['HUGGINGFACE_TOKEN', 'NEWS_API_KEY', 'OPENAI_API_KEY']
    
    print("Required variables:")
    all_required = True
    for var in required_vars:
        value = os.getenv(var, 'NOT_SET')
        if value != 'NOT_SET':
            masked = value[:8] + '...' if len(value) > 8 else value
            print(f"  ✅ {var}: {masked}")
        else:
            print(f"  ❌ {var}: NOT_SET")
            all_required = False
    
    print("\nOptional variables:")
    for var in optional_vars:
        value = os.getenv(var, 'NOT_SET')
        if value != 'NOT_SET':
            masked = value[:8] + '...' if len(value) > 8 else value
            print(f"  ✅ {var}: {masked}")
        else:
            print(f"  ⚪ {var}: NOT_SET (optional)")
    
    return all_required

def test_news_fetching():
    """Test news fetching functionality"""
    print(f"\n📰 Testing News Fetching")
    print("=" * 25)
    
    try:
        from api_linkedin_bot import APILinkedInBot
        bot = APILinkedInBot()
        
        articles = bot.fetch_tech_news()
        
        if articles:
            print(f"✅ Fetched {len(articles)} articles")
            for i, article in enumerate(articles):
                print(f"  {i+1}. {article['title'][:60]}...")
            return True
        else:
            print("❌ No articles fetched")
            return False
            
    except Exception as e:
        print(f"❌ Error fetching news: {str(e)}")
        return False

def test_content_generation():
    """Test content generation"""
    print(f"\n✨ Testing Content Generation")
    print("=" * 30)
    
    try:
        from api_linkedin_bot import APILinkedInBot
        bot = APILinkedInBot()
        
        # Test with sample article
        sample_article = {
            'title': 'AI Revolution: New Breakthrough in Machine Learning',
            'description': 'Scientists have developed a new AI model that can understand complex patterns.',
            'url': 'https://example.com',
            'source': 'Tech News'
        }
        
        content = bot.generate_content_with_api(sample_article)
        
        if content:
            print(f"✅ Generated content ({len(content)} characters)")
            print("\nSample content:")
            print("-" * 40)
            print(content[:200] + "..." if len(content) > 200 else content)
            print("-" * 40)
            return True
        else:
            print("❌ Content generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error generating content: {str(e)}")
        return False

def test_linkedin_connection():
    """Test LinkedIn API connection"""
    print(f"\n🔗 Testing LinkedIn Connection")
    print("=" * 30)
    
    try:
        import requests
        
        access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        if not access_token:
            print("❌ No LinkedIn access token")
            return False
        
        # Test getting profile
        url = "https://api.linkedin.com/v2/people/~"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            name = f"{data.get('localizedFirstName', '')} {data.get('localizedLastName', '')}".strip()
            print(f"✅ Connected to LinkedIn profile: {name or 'Unknown'}")
            return True
        else:
            print(f"❌ LinkedIn API error: {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LinkedIn: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🧪 API-Based LinkedIn Bot Test")
    print("=" * 35)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded from .env file")
    except ImportError:
        print("⚠️ python-dotenv not available, using system environment")
    except Exception as e:
        print(f"⚠️ Could not load .env: {str(e)}")
    
    # Run tests
    tests = [
        ("Environment", test_environment),
        ("News Fetching", test_news_fetching),
        ("Content Generation", test_content_generation),
        ("LinkedIn Connection", test_linkedin_connection)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 20)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for automation!")
    else:
        print("⚠️ Some tests failed. Check the issues above.")
        
        if not results.get("Environment", False):
            print("\n💡 Quick fix: Make sure your .env file has:")
            print("   LINKEDIN_ACCESS_TOKEN=your_token")
            print("   LINKEDIN_CLIENT_ID=your_client_id")
            print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🚀 Ready to run: python api_linkedin_bot.py")
    else:
        print(f"\n🔧 Fix the issues above first")