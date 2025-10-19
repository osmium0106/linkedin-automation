"""
Authentication Helper Script
Helps users set up LinkedIn OAuth authentication
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_poster import LinkedInPoster, start_oauth_server
from config import Config
from loguru import logger

def main():
    """Run LinkedIn OAuth authentication setup"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║              🔐 LinkedIn OAuth Setup Helper 🔐             ║
    ║                                                            ║
    ║  This script will help you authenticate with LinkedIn API  ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Check if basic config is available
        if not Config.LINKEDIN_CLIENT_ID or not Config.LINKEDIN_CLIENT_SECRET:
            print("❌ LinkedIn Client ID and Client Secret are required!")
            print("📝 Please follow these steps:")
            print("   1. Go to https://www.linkedin.com/developers/apps")
            print("   2. Create a new app or use existing one")
            print("   3. Copy Client ID and Client Secret")
            print("   4. Add them to your .env file")
            print("   5. Run this script again")
            return False
        
        print(f"✅ Found LinkedIn Client ID: {Config.LINKEDIN_CLIENT_ID}")
        
        # Check if we already have a token
        if Config.LINKEDIN_ACCESS_TOKEN:
            print(f"✅ Access token found: {Config.LINKEDIN_ACCESS_TOKEN[:20]}...")
            
            # Test the existing token
            try:
                linkedin_poster = LinkedInPoster()
                profile = linkedin_poster.get_user_profile()
                print(f"✅ Token is valid! Connected to profile: {profile.get('id', 'Unknown')}")
                print("🎉 Authentication is already set up!")
                return True
                
            except Exception as e:
                print(f"❌ Existing token is invalid: {str(e)}")
                print("🔄 Will generate a new token...")
        
        # Start OAuth flow
        print("🔄 Starting LinkedIn OAuth authentication...")
        print("📝 Make sure your LinkedIn app has these settings:")
        print(f"   • Redirect URI: {Config.LINKEDIN_REDIRECT_URI}")
        print("   • Required products: Sign In with LinkedIn, Share on LinkedIn")
        print("")
        
        linkedin_poster = LinkedInPoster()
        start_oauth_server(linkedin_poster)
        
        print("🎉 Authentication completed!")
        print("📝 Don't forget to add the access token to your .env file!")
        
        return True
        
    except KeyboardInterrupt:
        print("\\n⏹️  Authentication cancelled by user")
        return False
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        print(f"❌ Authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)