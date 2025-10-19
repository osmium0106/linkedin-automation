#!/usr/bin/env python3
"""
Quick LinkedIn API test without loading AI models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_linkedin_poster import AutoLinkedInPoster

def main():
    print("\n🔧 LINKEDIN API ACCESS TEST")
    print("=" * 40)
    
    try:
        poster = AutoLinkedInPoster()
        results = poster.test_api_access()
        
        print(f"Token Valid: {'✅' if results['token_valid'] else '❌'}")
        print(f"User Info Access: {'✅' if results['user_info'] else '❌'}")
        print(f"Share API: {'✅' if results['share_api'] else '❌'}")
        print(f"UGC Posts API: {'✅' if results['ugc_api'] else '❌'}")
        
        if results["recommendations"]:
            print(f"\n💡 Recommendations:")
            for rec in results["recommendations"]:
                print(f"   • {rec}")
        
        # Determine overall status
        if results["token_valid"] and (results["share_api"] or results["ugc_api"]):
            print(f"\n✅ AUTOMATIC POSTING: READY")
            print(f"💡 Your bot can post automatically to LinkedIn!")
            
            # Ask if user wants to test posting
            test_post = input("\n🤔 Would you like to test automatic posting? (y/n): ").lower().strip()
            if test_post == 'y':
                test_content = "🤖 Test post from LinkedIn automation bot! Testing automatic posting functionality. #TestPost #LinkedInBot #Automation"
                success = poster.auto_post(test_content)
                if success:
                    print("✅ Test post successful!")
                else:
                    print("❌ Test post failed!")
                    
        elif results["token_valid"]:
            print(f"\n⚠️ AUTOMATIC POSTING: LIMITED")
            print(f"💡 Token works but posting may require browser automation")
            
            # Ask if user wants to try browser automation
            test_browser = input("\n🤔 Would you like to test browser automation posting? (y/n): ").lower().strip()
            if test_browser == 'y':
                test_content = "🤖 Test post from LinkedIn automation bot! Testing browser automation functionality. #TestPost #LinkedInBot #BrowserAutomation"
                success = poster.post_with_browser_automation(test_content)
                if success:
                    print("✅ Browser automation test successful!")
                else:
                    print("❌ Browser automation test failed!")
        else:
            print(f"\n❌ AUTOMATIC POSTING: NOT READY")
            print(f"💡 Run 'python setup_auth.py' to get LinkedIn access token")
        
        return results["token_valid"]
        
    except Exception as e:
        print(f"❌ Error testing LinkedIn API: {str(e)}")
        return False

if __name__ == "__main__":
    main()