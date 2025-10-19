"""
LinkedIn Poster Module
Handles LinkedIn OAuth authentication and posting via LinkedIn API
"""

import os
import requests
import json
from typing import Dict, Optional
from datetime import datetime
import base64
from loguru import logger
from config import Config

class LinkedInPoster:
    def __init__(self):
        self.config = Config()
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = Config.LINKEDIN_REDIRECT_URI
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        
        # LinkedIn API endpoints
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.api_base = "https://api.linkedin.com/v2"
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """Validate LinkedIn API configuration"""
        if not self.client_id or not self.client_secret:
            raise ValueError("LinkedIn Client ID and Client Secret are required")
        
        if not self.access_token:
            logger.warning("No LinkedIn access token found. You'll need to authenticate first.")
    
    def get_authorization_url(self) -> str:
        """
        Generate LinkedIn OAuth authorization URL
        
        Returns:
            Authorization URL for user to visit
        """
        scope = "w_member_social"  # Only use scopes that are authorized
        
        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
            "state": "linkedin_bot_auth"  # CSRF protection
        }
        
        auth_url = f"{self.auth_url}?" + "&".join([f"{k}={v}" for k, v in auth_params.items()])
        
        logger.info(f"Generated authorization URL: {auth_url}")
        return auth_url
    
    def get_access_token(self, authorization_code: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code: Code received from LinkedIn OAuth callback
            
        Returns:
            Dictionary containing access token and related information
        """
        try:
            token_data = {
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            
            response = requests.post(self.token_url, data=token_data, headers=headers)
            response.raise_for_status()
            
            token_info = response.json()
            
            # Store the access token
            self.access_token = token_info.get('access_token')
            
            logger.success("Successfully obtained LinkedIn access token")
            logger.info("Don't forget to add this token to your .env file!")
            
            return token_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting access token: {str(e)}")
            raise
    
    def get_user_profile(self) -> Dict:
        """
        Get the authenticated user's LinkedIn profile information
        
        Returns:
            User profile data
        """
        if not self.access_token:
            raise ValueError("Access token required. Please authenticate first.")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Get basic profile info
            profile_url = f"{self.api_base}/people/~"
            response = requests.get(profile_url, headers=headers)
            response.raise_for_status()
            
            profile_data = response.json()
            logger.info(f"Retrieved profile for user: {profile_data.get('id', 'Unknown')}")
            
            return profile_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting user profile: {str(e)}")
            raise
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """
        Upload an image to LinkedIn for use in posts
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Asset URN for the uploaded image
        """
        if not self.access_token:
            raise ValueError("Access token required")
        
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # Step 1: Register upload
            register_upload_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{self.get_user_profile()['id']}",
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            
            register_url = f"{self.api_base}/assets?action=registerUpload"
            register_response = requests.post(register_url, headers=headers, json=register_upload_data)
            register_response.raise_for_status()
            
            register_result = register_response.json()
            asset_id = register_result['value']['asset']
            upload_url = register_result['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            
            # Step 2: Upload the image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            upload_headers = {"Authorization": f"Bearer {self.access_token}"}
            upload_response = requests.put(upload_url, data=image_data, headers=upload_headers)
            upload_response.raise_for_status()
            
            logger.success(f"Successfully uploaded image: {image_path}")
            return asset_id
            
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return None
    
    def create_text_post(self, text: str) -> Dict:
        """
        Create a text-only LinkedIn post
        
        Args:
            text: Post content
            
        Returns:
            Response from LinkedIn API
        """
        if not self.access_token:
            raise ValueError("Access token required")
        
        try:
            # Use a simple person URN since we can't get profile
            # This works with w_member_social scope
            person_urn = "urn:li:person:~"  # Simplified approach
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            post_data = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            post_url = f"{self.api_base}/ugcPosts"
            response = requests.post(post_url, headers=headers, json=post_data)
            response.raise_for_status()
            
            result = response.json()
            logger.success("Successfully posted text content to LinkedIn")
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating text post: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            raise
    
    def create_image_post(self, text: str, image_path: str) -> Dict:
        """
        Create a LinkedIn post with image
        
        Args:
            text: Post content
            image_path: Path to the image file
            
        Returns:
            Response from LinkedIn API
        """
        if not self.access_token:
            raise ValueError("Access token required")
        
        try:
            # Upload the image first
            asset_urn = self.upload_image(image_path)
            if not asset_urn:
                raise Exception("Failed to upload image")
            
            user_profile = self.get_user_profile()
            person_urn = f"urn:li:person:{user_profile['id']}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            post_data = {
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Generated image for LinkedIn post"
                                },
                                "media": asset_urn,
                                "title": {
                                    "text": "LinkedIn Automation Bot"
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            post_url = f"{self.api_base}/ugcPosts"
            response = requests.post(post_url, headers=headers, json=post_data)
            response.raise_for_status()
            
            result = response.json()
            logger.success(f"Successfully posted content with image to LinkedIn: {image_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating image post: {str(e)}")
            # Fallback to text-only post if image upload fails
            logger.info("Falling back to text-only post...")
            return self.create_text_post(text)
    
    def create_post(self, text: str, image_path: Optional[str] = None) -> Dict:
        """
        Create a LinkedIn post (text-only for now due to scope limitations)
        
        Args:
            text: Post content
            image_path: Optional path to image file (currently not supported due to API limitations)
            
        Returns:
            Response from LinkedIn API
        """
        try:
            # For now, only create text posts due to API scope limitations
            if image_path:
                logger.warning("Image posting not available with current API scopes. Creating text-only post.")
            
            return self.create_text_post(text)
                
        except Exception as e:
            logger.error(f"Error creating LinkedIn post: {str(e)}")
            raise
    
    def schedule_post(self, text: str, image_path: Optional[str] = None, scheduled_time: Optional[datetime] = None) -> Dict:
        """
        Schedule a LinkedIn post for later (Note: LinkedIn API has limited scheduling support)
        
        Args:
            text: Post content
            image_path: Optional path to image file
            scheduled_time: When to schedule the post
            
        Returns:
            Response from LinkedIn API
        """
        # Note: LinkedIn API doesn't support scheduling directly
        # This would require a job scheduler like Celery or similar
        logger.warning("LinkedIn API doesn't support native scheduling. Post will be created immediately.")
        return self.create_post(text, image_path)
    
    def get_post_analytics(self, post_id: str) -> Dict:
        """
        Get analytics for a specific post (requires additional permissions)
        
        Args:
            post_id: LinkedIn post ID
            
        Returns:
            Post analytics data
        """
        if not self.access_token:
            raise ValueError("Access token required")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # This endpoint requires additional permissions
            analytics_url = f"{self.api_base}/socialActions/{post_id}"
            response = requests.get(analytics_url, headers=headers)
            response.raise_for_status()
            
            analytics_data = response.json()
            logger.info(f"Retrieved analytics for post: {post_id}")
            
            return analytics_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting post analytics: {str(e)}")
            raise

# OAuth helper functions
def start_oauth_server(linkedin_poster: LinkedInPoster):
    """
    Start a simple HTTP server to handle OAuth callback
    This is a helper function for the authentication flow
    """
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    import webbrowser
    
    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith('/callback'):
                # Parse the authorization code from the callback
                parsed_url = urlparse(self.path)
                params = parse_qs(parsed_url.query)
                
                if 'code' in params:
                    auth_code = params['code'][0]
                    try:
                        token_info = linkedin_poster.get_access_token(auth_code)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        success_html = f"""
                        <html>
                        <body>
                            <h2>✅ LinkedIn Authentication Successful!</h2>
                            <p>Access token obtained successfully.</p>
                            <p><strong>Your access token:</strong></p>
                            <code>{token_info.get('access_token', 'Not found')}</code>
                            <p>Add this token to your .env file as LINKEDIN_ACCESS_TOKEN</p>
                            <p>You can close this window now.</p>
                        </body>
                        </html>
                        """
                        
                        self.wfile.write(success_html.encode())
                        
                    except Exception as e:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        error_html = f"<html><body><h2>❌ Error: {str(e)}</h2></body></html>"
                        self.wfile.write(error_html.encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    error_html = "<html><body><h2>❌ No authorization code received</h2></body></html>"
                    self.wfile.write(error_html.encode())
            else:
                self.send_response(404)
                self.end_headers()
    
    # Start server
    server = HTTPServer(('localhost', 8000), OAuthHandler)
    
    # Open browser to authorization URL
    auth_url = linkedin_poster.get_authorization_url()
    webbrowser.open(auth_url)
    
    print(f"🔗 Opening LinkedIn authorization URL: {auth_url}")
    print("🖥️  Starting OAuth callback server on http://localhost:8000")
    print("👆 Click the link above if it doesn't open automatically")
    print("⏳ Waiting for authorization...")
    
    # Handle one request (the callback)
    server.handle_request()
    server.server_close()

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logger.add("logs/linkedin_poster.log", rotation="1 day", retention="7 days")
    
    try:
        linkedin_poster = LinkedInPoster()
        
        print("LinkedIn Poster Module Test")
        print("=" * 40)
        
        # Check if we have an access token
        if not linkedin_poster.access_token:
            print("❌ No LinkedIn access token found.")
            print("🔄 Starting OAuth flow...")
            
            # Start OAuth flow
            start_oauth_server(linkedin_poster)
        else:
            print("✅ LinkedIn access token found!")
            
            # Test getting user profile
            try:
                profile = linkedin_poster.get_user_profile()
                print(f"✅ Connected to LinkedIn profile: {profile.get('id', 'Unknown')}")
                
                # Test creating a simple post
                test_post_text = "🤖 Testing LinkedIn automation bot! This post was created automatically using Python. #LinkedInAPI #Automation #TechTest"
                
                print("🚀 Creating test post...")
                result = linkedin_poster.create_text_post(test_post_text)
                print(f"✅ Test post created successfully: {result.get('id', 'Unknown ID')}")
                
            except Exception as e:
                print(f"❌ Error testing LinkedIn API: {str(e)}")
                
    except Exception as e:
        logger.error(f"Error in LinkedIn poster test: {str(e)}")
        print(f"Error: {str(e)}")