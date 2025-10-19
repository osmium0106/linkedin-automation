#!/usr/bin/env python3"""

"""LinkedIn Automation Bot - Main Script

Telegram LinkedIn Content AutomationOrchestrates news fetching, content generation, and LinkedIn posting

Main entry point for the automation system."""

"""

import os

import subprocessimport sys

import sysimport traceback

from datetime import datetime, timedelta

def main():from typing import Optional, Dict

    """Run the Telegram automation script."""import schedule

    try:import time

        print("🤖 Starting Telegram LinkedIn Content Automation...")from loguru import logger

        result = subprocess.run([sys.executable, "test_telegram_automation.py"], 

                              capture_output=True, text=True)# Import our custom modules

        from config import Config

        if result.returncode == 0:from news_fetcher import NewsFetcher

            print("✅ Automation completed successfully!")from caption_generator import CaptionGenerator

            print(result.stdout)from image_generator import ImageGenerator

        else:from linkedin_content_manager import LinkedInContentManager

            print("❌ Automation failed!")from linkedin_poster import LinkedInPoster

            print(result.stderr)from auto_linkedin_poster import AutoLinkedInPoster, post_to_linkedin_auto

            return 1

            class LinkedInBot:

    except Exception as e:    def __init__(self):

        print(f"❌ Error running automation: {e}")        """Initialize the LinkedIn automation bot"""

        return 1        try:

                # Load configuration

    return 0            Config.validate_config()

            

if __name__ == "__main__":            # Initialize components

    exit(main())            self.news_fetcher = NewsFetcher()
            self.caption_generator = CaptionGenerator()
            self.image_generator = ImageGenerator()
            self.content_manager = LinkedInContentManager()
            
            # Initialize both manual and automatic LinkedIn posters
            self.linkedin_poster = LinkedInPoster()
            self.auto_poster = AutoLinkedInPoster()
            
            # Create necessary directories
            os.makedirs(Config.IMAGES_DIR, exist_ok=True)
            os.makedirs(Config.LOGS_DIR, exist_ok=True)
            
            # Configure logging
            self._setup_logging()
            
            logger.success("LinkedIn automation bot initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize LinkedIn bot: {str(e)}")
            raise
    
    def _setup_logging(self):
        """Configure logging for the bot"""
        # Remove default handler
        logger.remove()
        
        # Add console handler with nice formatting
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        
        # Add file handler
        logger.add(
            os.path.join(Config.LOGS_DIR, "linkedin_bot_{time:YYYY-MM-DD}.log"),
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="1 day",
            retention="7 days"
        )
        
        # Add error file handler
        logger.add(
            os.path.join(Config.LOGS_DIR, "linkedin_bot_errors_{time:YYYY-MM-DD}.log"),
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="1 day",
            retention="30 days"
        )
    
    def generate_content(self) -> Optional[Dict]:
        """
        Generate content for LinkedIn post
        
        Returns:
            Dictionary containing caption and image path, or None if failed
        """
        try:
            logger.info("🔄 Starting content generation process...")
            
            # Step 1: Fetch trending news
            logger.info("📰 Fetching trending news...")
            articles = self.news_fetcher.get_trending_news(num_articles_per_topic=3)
            
            if not articles:
                logger.error("No articles found from news sources")
                return None
            
            # Step 2: Select an interesting article
            selected_article = self.news_fetcher.select_random_article(articles)
            logger.info(f"📄 Selected article: {selected_article['title'][:100]}...")
            
            # Step 3: Generate LinkedIn caption
            logger.info("✍️  Generating LinkedIn caption...")
            caption = self.caption_generator.create_linkedin_post(selected_article)
            
            if not caption:
                logger.error("Failed to generate caption")
                return None
            
            logger.success(f"✅ Generated caption ({len(caption)} characters)")
            
            # Step 4: Generate or create image
            logger.info("🎨 Generating post image...")
            image_path = self.image_generator.generate_image(selected_article)
            
            if image_path:
                logger.success(f"✅ Generated image: {image_path}")
            else:
                logger.warning("⚠️  Image generation failed, will post text-only")
            
            return {
                'caption': caption,
                'image_path': image_path,
                'article': selected_article,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating content: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def post_to_linkedin(self, content: Dict, auto_post: bool = True) -> bool:
        """
        Post content to LinkedIn automatically or prepare for manual posting
        
        Args:
            content: Dictionary containing caption and image path
            auto_post: If True, attempt automatic posting. If False, just save for manual posting.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            caption = content['caption']
            image_path = content.get('image_path')
            article_title = content['article']['title']
            
            if auto_post:
                logger.info("🚀 Attempting automatic LinkedIn posting...")
                
                # Try automatic posting first
                success = self.auto_poster.auto_post(caption, image_path)
                
                if success:
                    logger.success("✅ Successfully posted to LinkedIn automatically!")
                    
                    # Log post details
                    logger.info(f"📊 Posted content details:")
                    logger.info(f"   Caption length: {len(caption)} characters")
                    logger.info(f"   Has image: {'Yes' if image_path else 'No'}")
                    logger.info(f"   Article title: {article_title}")
                    
                    return True
                else:
                    logger.warning("⚠️ Automatic posting failed, falling back to manual posting preparation...")
            
            # If auto posting failed or was disabled, prepare for manual posting
            logger.info("📤 Preparing content for manual LinkedIn posting...")
            
            result = self.content_manager.save_content_for_posting(
                content=caption,
                image_path=image_path,
                topic="News Automation"
            )
            
            if result:
                logger.success(f"✅ Content prepared for LinkedIn posting!")
                
                # Log post details
                logger.info(f"📊 Content details:")
                logger.info(f"   Caption length: {len(caption)} characters")
                logger.info(f"   Has image: {'Yes' if image_path else 'No'}")
                logger.info(f"   Article title: {article_title}")
                logger.info(f"   Text file: {result['text_file']}")
                
                if 'image_file' in result:
                    logger.info(f"   Image file: {result['image_file']}")
                
                # Show posting options only if auto posting failed
                if not auto_post or not success:
                    print(f"\n🎉 CONTENT READY FOR LINKEDIN POSTING!")
                    print(f"📄 Text file: {result['text_file']}")
                    print(f"📊 Character count: {result['character_count']}")
                    
                    if 'image_file' in result:
                        print(f"📸 Image file: {result['image_file']}")
                    
                    print(f"\n🚀 QUICK POSTING OPTIONS:")
                    print(f"1. 📋 Copy content from: {result['text_file']}")
                    print(f"2. 🔗 Quick share URL: {result['share_url']}")
                    print(f"3. 📖 Full guide: {result['instructions_file']}")
                    print(f"4. 💻 Manual: Go to LinkedIn.com and create a post")
                    
                    print(f"\n💡 TIP: Use LinkedIn mobile app for easier image posting!")
                
                return True
            else:
                logger.error("❌ Failed to prepare content for posting")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error posting to LinkedIn: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def run_once(self, auto_post: bool = True) -> bool:
        """
        Run the bot once (fetch news, generate content, post)
        
        Args:
            auto_post: If True, attempt automatic posting. If False, just prepare for manual posting.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("🚀 Starting LinkedIn automation bot run...")
            start_time = datetime.now()
            
            # Generate content
            content = self.generate_content()
            if not content:
                logger.error("❌ Content generation failed")
                return False
            
            # Post to LinkedIn (automatically or prepare for manual)
            success = self.post_to_linkedin(content, auto_post=auto_post)
            
            # Calculate duration
            duration = datetime.now() - start_time
            
            if success:
                mode = "with automatic posting" if auto_post else "with content preparation"
                logger.success(f"🎉 Bot run completed successfully {mode} in {duration.total_seconds():.2f} seconds!")
            else:
                logger.error(f"❌ Bot run failed after {duration.total_seconds():.2f} seconds")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Unexpected error in bot run: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def schedule_posts(self):
        """Schedule posts according to configuration"""
        try:
            logger.info("⏰ Setting up post scheduling...")
            
            # Clear any existing scheduled jobs
            schedule.clear()
            
            # Schedule posts at configured times
            for post_time in Config.POSTING_TIMES:
                schedule.every().day.at(post_time).do(self.run_once)
                logger.info(f"📅 Scheduled daily post at {post_time}")
            
            logger.success(f"✅ Scheduled {len(Config.POSTING_TIMES)} daily posts")
            
            # Run the scheduler
            logger.info("🔄 Starting scheduler... Press Ctrl+C to stop.")
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.info("⏹️  Scheduler stopped by user")
        except Exception as e:
            logger.error(f"❌ Error in scheduler: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def test_components(self) -> bool:
        """
        Test all bot components without posting to LinkedIn
        
        Returns:
            True if all components work, False otherwise
        """
        try:
            logger.info("🧪 Testing bot components...")
            
            # Test 1: News fetcher
            logger.info("1️⃣  Testing news fetcher...")
            articles = self.news_fetcher.get_trending_news(num_articles_per_topic=1)
            if not articles:
                logger.error("❌ News fetcher test failed")
                return False
            logger.success("✅ News fetcher working")
            
            # Test 2: Caption generator
            logger.info("2️⃣  Testing caption generator...")
            test_article = articles[0] if articles else {
                'title': 'Test AI Article',
                'description': 'Testing the LinkedIn bot caption generation.',
                'topic': 'technology',
                'source': 'Test Source'
            }
            
            caption = self.caption_generator.create_linkedin_post(test_article)
            if not caption:
                logger.error("❌ Caption generator test failed")
                return False
            logger.success(f"✅ Caption generator working (generated {len(caption)} chars)")
            
            # Test 3: Image generator
            logger.info("3️⃣  Testing image generator...")
            image_path = self.image_generator.generate_image(test_article)
            if image_path and os.path.exists(image_path):
                logger.success(f"✅ Image generator working (saved to {image_path})")
            else:
                logger.warning("⚠️  Image generator using fallback method")
            
            # Test 4: LinkedIn poster (just check auth)
            logger.info("4️⃣  Testing LinkedIn authentication...")
            if not self.linkedin_poster.access_token:
                logger.warning("⚠️  No LinkedIn access token - authentication required")
                return False
            
            try:
                profile = self.linkedin_poster.get_user_profile()
                logger.success(f"✅ LinkedIn authentication working (User: {profile.get('id', 'Unknown')})")
            except Exception as e:
                logger.error(f"❌ LinkedIn authentication failed: {str(e)}")
                return False
            
            logger.success("🎉 All component tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Component test failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def test_linkedin_api(self):
        """Test LinkedIn API access and posting capabilities"""
        try:
            logger.info("🧪 Testing LinkedIn API access...")
            results = self.auto_poster.test_api_access()
            
            print(f"\n🔍 LINKEDIN API TEST RESULTS")
            print(f"{'='*40}")
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
            elif results["token_valid"]:
                print(f"\n⚠️ AUTOMATIC POSTING: LIMITED")
                print(f"💡 Token works but posting may require browser automation")
            else:
                print(f"\n❌ AUTOMATIC POSTING: NOT READY")
                print(f"💡 Run 'python setup_auth.py' to get LinkedIn access token")
            
            return results["token_valid"]
            
        except Exception as e:
            logger.error(f"❌ Error testing LinkedIn API: {str(e)}")
            return False
    
    def manual_post_auto(self):
        """Manually trigger an automatic post"""
        logger.info("� Manual automatic post triggered...")
        success = self.run_once(auto_post=True)
        if success:
            logger.success("✅ Manual automatic post completed successfully!")
        else:
            logger.error("❌ Manual automatic post failed!")
        return success
    
    def manual_post_manual(self):
        """Manually trigger content generation for manual posting"""
        logger.info("📝 Manual content generation triggered...")
        success = self.run_once(auto_post=False)
        if success:
            logger.success("✅ Manual content generation completed successfully!")
        else:
            logger.error("❌ Manual content generation failed!")
        return success
    
    def show_content_summary(self):
        """Show summary of generated content ready for posting"""
        try:
            logger.info("📊 Getting content summary...")
            summary = self.content_manager.get_posting_summary()
            
            print(f"\n📋 CONTENT READY FOR POSTING")
            print(f"{'='*50}")
            print(f"📄 Total posts ready: {summary['total_posts']}")
            
            if summary['posts_by_topic']:
                print(f"\n📁 Posts by topic:")
                for topic, count in summary['posts_by_topic'].items():
                    print(f"   • {topic}: {count} posts")
            
            if summary['recent_posts']:
                print(f"\n🕒 Recent posts:")
                for post in summary['recent_posts'][:5]:  # Show last 5
                    print(f"   • {post['created']} - {post['topic']}")
                    print(f"     📄 {post['file']}")
            
            if summary['total_posts'] > 0:
                print(f"\n💡 TIP: Check the 'ready_to_post' folder for your content!")
                print(f"🔗 Each post has a posting guide with quick share URLs")
            else:
                print(f"\n🤔 No content ready yet. Run 'python main.py generate' to create some!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error getting content summary: {str(e)}")
            return False
    
    def open_posting_folder(self):
        """Open the posting folder in file explorer"""
        try:
            import subprocess
            import platform
            
            posting_dir = self.content_manager.output_dir
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", posting_dir])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", posting_dir])
            else:  # Linux
                subprocess.run(["xdg-open", posting_dir])
            
            logger.success(f"📂 Opened posting folder: {posting_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error opening posting folder: {str(e)}")
            return False

def main():
    """Main function to run the LinkedIn automation bot"""
    
    # ASCII Art Banner
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║            🤖 LinkedIn Automation Bot 🤖             ║
    ║                                                      ║
    ║  📰 Fetches News  →  🤖 Generates AI Content  →  📤  ║
    ╚══════════════════════════════════════════════════════╝
    """
    print(banner)
    
    try:
        # Initialize the bot
        bot = LinkedInBot()
        
        # Parse command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == "test":
                print("🧪 Running component tests...")
                success = bot.test_components()
                sys.exit(0 if success else 1)
                
            elif command == "api":
                print("🔧 Testing LinkedIn API access...")
                success = bot.test_linkedin_api()
                sys.exit(0 if success else 1)
                
            elif command == "post":
                print("🚀 Creating automatic post...")
                success = bot.manual_post_auto()
                sys.exit(0 if success else 1)
                
            elif command == "manual":
                print("� Creating content for manual posting...")
                success = bot.manual_post_manual()
                sys.exit(0 if success else 1)
                
            elif command == "schedule":
                print("⏰ Starting scheduled mode...")
                bot.schedule_posts()
                
            elif command == "generate":
                print("🎨 Generating content only (no posting)...")
                content = bot.generate_content()
                if content:
                    print(f"✅ Content generated successfully!")
                    print(f"Caption: {content['caption'][:200]}...")
                    print(f"Image: {content.get('image_path', 'None')}")
                else:
                    print("❌ Content generation failed!")
                sys.exit(0 if content else 1)
                
            elif command == "summary":
                print("📊 Showing content summary...")
                success = bot.show_content_summary()
                sys.exit(0 if success else 1)
                
            elif command == "open":
                print("📂 Opening posting folder...")
                success = bot.open_posting_folder()
                sys.exit(0 if success else 1)
                
            else:
                print(f"❌ Unknown command: {command}")
                print("Available commands: test, api, post, manual, schedule, generate, summary, open")
                sys.exit(1)
        else:
            # No arguments - show help
            print("📖 LinkedIn Automation Bot Usage:")
            print("")
            print("🚀 AUTOMATIC POSTING:")
            print("   python main.py post      - Generate content and post automatically")
            print("   python main.py api       - Test LinkedIn API access")
            print("")
            print("📝 MANUAL POSTING:")
            print("   python main.py manual    - Generate content for manual posting")
            print("   python main.py summary   - Show content ready for posting")
            print("   python main.py open      - Open posting folder")
            print("")
            print("🔧 UTILITIES:")
            print("   python main.py test      - Test all components")
            print("   python main.py generate  - Generate content only")
            print("   python main.py schedule  - Start scheduled posting")
            print("")
            print("🔧 Setup Instructions:")
            print("   1. Install: pip install -r requirements.txt")
            print("   2. Setup LinkedIn: python setup_auth.py")
            print("   3. Test API: python main.py api")
            print("   4. Create post: python main.py post")
            
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
        
    except Exception as e:
        logger.error(f"💥 Critical error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main()