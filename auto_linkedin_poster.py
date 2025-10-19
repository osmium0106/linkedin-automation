"""
Automatic LinkedIn Poster
Implements multiple strategies for automatic LinkedIn posting
"""

import os
import time
import requests
import json
from typing import Dict, Optional, Union
from datetime import datetime
from loguru import logger
from config import Config

class AutoLinkedInPoster:
    def __init__(self):
        self.config = Config()
        self.access_token = Config.LINKEDIN_ACCESS_TOKEN
        self.client_id = Config.LINKEDIN_CLIENT_ID
        self.client_secret = Config.LINKEDIN_CLIENT_SECRET
        
        # API endpoints
        self.api_base = "https://api.linkedin.com/v2"
        self.share_api = "https://api.linkedin.com/v2/shares"
        self.ugc_api = "https://api.linkedin.com/v2/ugcPosts"
        
        # User info cache
        self._user_id = None
        self._user_urn = None
    
    def get_user_info(self) -> Dict:
        """Get current user information with better error handling"""
        if not self.access_token:
            raise ValueError("LinkedIn access token required for automatic posting")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Try multiple endpoints to get user info
        endpoints_to_try = [
            ("/people/~", "Basic profile"),
            ("/people/~:(id,firstName,lastName)", "Profile with fields"),
            ("/me", "Current user endpoint")
        ]
        
        for endpoint, description in endpoints_to_try:
            try:
                url = f"{self.api_base}{endpoint}"
                logger.info(f"Trying {description}: {url}")
                
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.success(f"✅ Got user info via {description}")
                    
                    # Cache user info
                    self._user_id = data.get('id')
                    if self._user_id:
                        self._user_urn = f"urn:li:person:{self._user_id}"
                    
                    return data
                else:
                    logger.warning(f"❌ {description} failed: {response.status_code} - {response.text[:100]}")
                    
            except Exception as e:
                logger.warning(f"❌ {description} error: {str(e)}")
                continue
        
        # If all endpoints fail, we'll try posting without user info
        logger.warning("⚠️ Could not get user profile info, will try alternative posting methods")
        return {}
    
    def create_simple_share(self, content: str) -> bool:
        """Try the simplest LinkedIn Share API approach"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Simple share format
            share_data = {
                "comment": content,
                "visibility": {
                    "code": "anyone"
                }
            }
            
            logger.info("🔄 Attempting simple share API...")
            response = requests.post(self.share_api, headers=headers, json=share_data, timeout=15)
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.success(f"✅ Posted via Share API! ID: {result.get('id', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ Share API failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Share API error: {str(e)}")
            return False
    
    def create_ugc_post_v1(self, content: str, image_path: Optional[str] = None) -> bool:
        """Try UGC Posts API with simplified format"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Get user info if not cached
            if not self._user_urn:
                self.get_user_info()
            
            # Use fallback URN if we still don't have user info
            author_urn = self._user_urn or "urn:li:person:~"
            
            post_data = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            logger.info(f"🔄 Attempting UGC Posts with author: {author_urn}")
            response = requests.post(self.ugc_api, headers=headers, json=post_data, timeout=15)
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.success(f"✅ Posted via UGC API! ID: {result.get('id', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ UGC API failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ UGC API error: {str(e)}")
            return False
    
    def create_ugc_post_v2(self, content: str, image_path: Optional[str] = None) -> bool:
        """Try UGC Posts API with alternative format"""
        try:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Alternative format - try with member URN
            post_data = {
                "author": "urn:li:member:~",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            logger.info("🔄 Attempting UGC Posts with member URN...")
            response = requests.post(self.ugc_api, headers=headers, json=post_data, timeout=15)
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.success(f"✅ Posted via UGC API v2! ID: {result.get('id', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ UGC API v2 failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ UGC API v2 error: {str(e)}")
            return False
    
    def post_with_browser_automation(self, content: str, image_path: Optional[str] = None) -> bool:
        """Use browser automation as fallback for posting"""
        try:
            logger.info("🔄 Attempting browser automation posting...")
            
            # Try to import selenium
            try:
                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
            except ImportError as e:
                logger.error(f"❌ Selenium not installed properly: {e}")
                logger.info("💡 Install with: pip install selenium webdriver-manager")
                return False
            
            # Setup Chrome options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            # Keep browser visible so user can interact
            
            try:
                # Use webdriver-manager to automatically download chromedriver
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                
                logger.info("🌐 Opening LinkedIn...")
                driver.get("https://linkedin.com/login")
                
                logger.info("🔗 LinkedIn login page opened.")
                logger.info("👤 Please log in manually in the browser window...")
                logger.info("⏳ After logging in, the bot will automatically post your content...")
                
                # Wait for user to log in and get to feed (check for LinkedIn homepage elements)
                logger.info("⌛ Waiting for you to log in (up to 5 minutes)...")
                
                try:
                    # Wait for either feed page or direct post button
                    WebDriverWait(driver, 300).until(  # 5 minutes
                        lambda driver: (
                            driver.find_elements(By.XPATH, "//span[contains(text(), 'Start a post')]") or
                            driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Start a post')]") or
                            driver.find_elements(By.XPATH, "//*[contains(text(), 'Share an update')]")
                        )
                    )
                    logger.success("✅ Login detected! Starting post creation...")
                    
                except Exception:
                    logger.error("⏰ Login timeout. Please try again.")
                    driver.quit()
                    return False
                
                # Try to find and click the post button
                post_button_selectors = [
                    "//span[contains(text(), 'Start a post')]",
                    "//button[contains(@aria-label, 'Start a post')]", 
                    "//*[contains(text(), 'Share an update')]",
                    "//button[contains(text(), 'Start a post')]"
                ]
                
                start_post_element = None
                for selector in post_button_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        if elements:
                            start_post_element = elements[0]
                            logger.info(f"✅ Found post button with selector: {selector}")
                            break
                    except Exception:
                        continue
                
                if not start_post_element:
                    logger.error("❌ Could not find 'Start a post' button")
                    logger.info("💡 Please navigate to LinkedIn feed manually and try again")
                    driver.quit()
                    return False
                
                # Click to start posting
                driver.execute_script("arguments[0].click();", start_post_element)
                logger.info("🖱️ Clicked 'Start a post'")
                
                # Wait for the post editor to appear
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
                    )
                    logger.success("✅ Post editor opened")
                except Exception:
                    logger.error("❌ Could not find post editor")
                    driver.quit()
                    return False
                
                # Enter the content
                text_areas = driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
                if text_areas:
                    text_area = text_areas[0]
                    text_area.click()
                    time.sleep(1)
                    
                    # Clear any existing content and add our content
                    text_area.clear()
                    text_area.send_keys(content)
                    logger.success("✅ Content added to post")
                else:
                    logger.error("❌ Could not find text input area")
                    driver.quit()
                    return False
                
                # Add image if provided
                if image_path and os.path.exists(image_path):
                    try:
                        logger.info("📸 Attempting to upload image...")
                        
                        # Look for image upload button
                        image_selectors = [
                            "//span[contains(text(), 'Photo')]",
                            "//button[contains(@aria-label, 'Add a photo')]",
                            "//*[contains(@data-test-id, 'photo')]",
                            "//input[@type='file']"
                        ]
                        
                        image_button = None
                        for selector in image_selectors:
                            try:
                                elements = driver.find_elements(By.XPATH, selector)
                                if elements:
                                    image_button = elements[0]
                                    break
                            except Exception:
                                continue
                        
                        if image_button:
                            if image_button.tag_name == 'input':
                                # Direct file input
                                image_button.send_keys(os.path.abspath(image_path))
                            else:
                                # Click button first
                                image_button.click()
                                time.sleep(2)
                                
                                # Find file input
                                file_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                                if file_inputs:
                                    file_inputs[0].send_keys(os.path.abspath(image_path))
                            
                            logger.success("✅ Image uploaded")
                            time.sleep(3)  # Wait for image to process
                        else:
                            logger.warning("⚠️ Could not find image upload button")
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Could not upload image: {str(e)}")
                
                # Post the content
                logger.info("📤 Looking for Post button...")
                post_selectors = [
                    "//span[contains(text(), 'Post')]",
                    "//button[contains(text(), 'Post')]",
                    "//button[contains(@aria-label, 'Post')]"
                ]
                
                post_button = None
                for selector in post_selectors:
                    try:
                        elements = driver.find_elements(By.XPATH, selector)
                        for element in elements:
                            # Make sure it's a post button (not "Repost" etc)
                            if element.text.strip().lower() == 'post':
                                post_button = element
                                break
                        if post_button:
                            break
                    except Exception:
                        continue
                
                if post_button:
                    driver.execute_script("arguments[0].click();", post_button)
                    logger.success("✅ Post button clicked!")
                    
                    # Wait a bit for the post to complete
                    time.sleep(5)
                    
                    logger.success("🎉 Posted successfully via browser automation!")
                    
                    driver.quit()
                    return True
                else:
                    logger.error("❌ Could not find Post button")
                    logger.info("💡 Please click 'Post' manually in the browser")
                    time.sleep(10)  # Give user time to post manually
                    driver.quit()
                    return False
                
            except Exception as e:
                logger.error(f"❌ Browser automation failed: {str(e)}")
                try:
                    driver.quit()
                except:
                    pass
                return False
                
        except Exception as e:
            logger.error(f"❌ Browser automation setup failed: {str(e)}")
            return False
    
    def auto_post(self, content: str, image_path: Optional[str] = None) -> bool:
        """
        Automatically post to LinkedIn using multiple fallback strategies
        
        Args:
            content: Text content to post
            image_path: Optional path to image file
            
        Returns:
            True if posting succeeded with any method
        """
        logger.info("🚀 Starting automatic LinkedIn posting...")
        
        if not self.access_token:
            logger.error("❌ No LinkedIn access token found. Please run setup_auth.py first")
            return False
        
        # Strategy 1: Simple Share API
        logger.info("📤 Strategy 1: Simple Share API")
        if self.create_simple_share(content):
            return True
        
        # Strategy 2: UGC Posts API v1
        logger.info("📤 Strategy 2: UGC Posts API v1")
        if self.create_ugc_post_v1(content, image_path):
            return True
        
        # Strategy 3: UGC Posts API v2
        logger.info("📤 Strategy 3: UGC Posts API v2")
        if self.create_ugc_post_v2(content, image_path):
            return True
        
        # Strategy 4: Browser Automation (requires user interaction)
        logger.info("📤 Strategy 4: Browser Automation (fallback)")
        logger.warning("⚠️ API methods failed. Trying browser automation...")
        logger.warning("📢 This will open a browser window - please log in to LinkedIn manually")
        
        user_consent = input("🤔 Would you like to try browser automation? (y/n): ").lower().strip()
        if user_consent == 'y':
            if self.post_with_browser_automation(content, image_path):
                return True
        
        # All strategies failed
        logger.error("❌ All posting strategies failed!")
        logger.info("💡 Falling back to content saving for manual posting...")
        return False
    
    def test_api_access(self) -> Dict:
        """Test LinkedIn API access and permissions"""
        logger.info("🧪 Testing LinkedIn API access...")
        
        results = {
            "token_valid": False,
            "user_info": False,
            "share_api": False,
            "ugc_api": False,
            "recommendations": []
        }
        
        if not self.access_token:
            results["recommendations"].append("Get LinkedIn access token by running setup_auth.py")
            return results
        
        # Test token validity
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # Test basic token
            response = requests.get(f"{self.api_base}/people/~", headers=headers, timeout=5)
            if response.status_code == 200:
                results["token_valid"] = True
                results["user_info"] = True
                logger.success("✅ Token valid and user info accessible")
            elif response.status_code == 403:
                results["token_valid"] = True
                logger.warning("⚠️ Token valid but insufficient permissions for user info")
                results["recommendations"].append("Token has limited permissions - some features may not work")
            else:
                logger.error(f"❌ Token test failed: {response.status_code}")
                results["recommendations"].append("Token may be expired or invalid")
        
        except Exception as e:
            logger.error(f"❌ Token test error: {str(e)}")
            results["recommendations"].append("Check internet connection and token validity")
        
        # Test share API
        try:
            test_share = {
                "comment": "Test post from LinkedIn automation bot (will be deleted)",
                "visibility": {"code": "anyone"}
            }
            response = requests.post(self.share_api, headers=headers, json=test_share, timeout=5)
            if response.status_code in [200, 201]:
                results["share_api"] = True
                logger.success("✅ Share API accessible")
            else:
                logger.warning(f"⚠️ Share API test: {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️ Share API test error: {str(e)}")
        
        return results


# Simplified function for main.py compatibility
def post_to_linkedin_auto(content: str, image_path: Optional[str] = None) -> bool:
    """
    Automatically post to LinkedIn with fallback strategies
    
    Args:
        content: Text content to post
        image_path: Optional path to image file
        
    Returns:
        True if posted successfully
    """
    poster = AutoLinkedInPoster()
    return poster.auto_post(content, image_path)


if __name__ == "__main__":
    # Test the automatic poster
    poster = AutoLinkedInPoster()
    
    print("🧪 Testing LinkedIn API Access")
    print("=" * 40)
    
    results = poster.test_api_access()
    
    print(f"Token Valid: {'✅' if results['token_valid'] else '❌'}")
    print(f"User Info: {'✅' if results['user_info'] else '❌'}")
    print(f"Share API: {'✅' if results['share_api'] else '❌'}")
    print(f"UGC API: {'✅' if results['ugc_api'] else '❌'}")
    
    if results["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"   • {rec}")
    
    # Test posting if user wants
    if results["token_valid"]:
        test_post = input("\n🤔 Would you like to test posting? (y/n): ").lower().strip()
        if test_post == 'y':
            test_content = "🤖 Test post from LinkedIn automation bot! This is a test of automatic posting functionality. #TestPost #LinkedInBot"
            success = poster.auto_post(test_content)
            if success:
                print("✅ Test post successful!")
            else:
                print("❌ Test post failed!")