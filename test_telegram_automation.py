#!/usr/bin/env python3
"""
Test Telegram Setup and Send LinkedIn Content
Verifies Telegram bot works and sends a test LinkedIn message
"""

import os
import requests
import json
from datetime import datetime

def test_telegram_bot():
    """Test if Telegram bot is working"""
    
    print("🤖 Testing Telegram Bot Setup")
    print("=" * 35)
    
    # Load from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️ python-dotenv not available, using system environment")
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print(f"🔑 Bot Token: {bot_token[:20] if bot_token else 'NOT FOUND'}...")
    print(f"💬 Chat ID: {chat_id}")
    
    if not bot_token or not chat_id:
        print("❌ Missing Telegram credentials in .env file")
        return False
    
    # Test bot info
    print(f"\n🧪 Testing bot connection...")
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                bot_name = bot_info['result']['first_name']
                bot_username = bot_info['result']['username']
                
                print(f"✅ Bot connection successful!")
                print(f"🤖 Bot Name: {bot_name}")
                print(f"📝 Bot Username: @{bot_username}")
            else:
                print(f"❌ Bot API error: {bot_info}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False
    
    # Send test message
    print(f"\n📤 Sending test message...")
    
    test_message = f"""🎉 TELEGRAM AUTOMATION WORKING!

✅ Your LinkedIn automation is now connected to Telegram!

🚀 You'll receive messages like this with:
• Professional LinkedIn content (from real tech news)
• Images when available  
• Step-by-step posting instructions

📅 Schedule: 3x daily automatically
• 2:30 PM IST (9 AM UTC)
• 7:30 PM IST (2 PM UTC)  
• 11:30 PM IST (6 PM UTC)

💡 Much more reliable than WhatsApp APIs!

🤖 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Reply with any emoji to confirm you received this! 🎊"""

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': test_message
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                print(f"✅ Test message sent successfully!")
                print(f"📱 Check your Telegram bot (@{bot_username}) for the message!")
                return True
            else:
                print(f"❌ Telegram API error: {result}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Send error: {str(e)}")
    
    return False

def send_linkedin_content():
    """Generate and send LinkedIn content via Telegram"""
    
    print(f"\n📝 Generating LinkedIn Content...")
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    # Generate fresh LinkedIn content
    try:
        from news_fetcher import NewsFetcher
        
        news_fetcher = NewsFetcher()
        articles = news_fetcher.fetch_tech_news()
        
        if articles:
            article = articles[0]  # Get the first article
            linkedin_content = f"""🚀 {article['title']}

💡 Key takeaways:
• {article['description'][:100]}...
• Fresh insights from leading tech sources
• Stay ahead with the latest industry trends

What are your thoughts on this development? Share below! 👇

#Technology #Innovation #TechNews #LinkedIn #AI #Business

📖 Read more: {article['link']}
📰 Source: {article['source']}
🕒 Generated: {datetime.now().strftime('%H:%M %d-%m-%Y')}"""
            
            image_info = {'url': article.get('image_url')} if article.get('image_url') else None
            print(f"✅ Content generated from: {article['source']}")
        else:
            raise Exception("No articles found")
        
    except Exception as e:
        print(f"⚠️ Content generation error: {e}")
        # Fallback content
        linkedin_content = f"""🚀 Innovation continues to reshape our digital world!

💡 Key insights for today:
• Technology advancement accelerates across industries
• Digital transformation remains a key business priority  
• Staying informed drives professional growth

What emerging technology has caught your attention recently? 

Share your thoughts in the comments! 👇

#Innovation #Technology #Future #LinkedIn #TechNews #AI

🕒 Generated: {datetime.now().strftime('%H:%M %d-%m-%Y')}"""
        image_info = None
    
    # Create Telegram message
    if image_info:
        telegram_message = f"""🚀 Fresh LinkedIn Content + Image Ready!

📝 COPY THIS TO LINKEDIN:
{linkedin_content}

📸 IMAGE AVAILABLE:
• File: {image_info['filename']}
• Size: {image_info['size_mb']} MB
• GitHub: {image_info['github_url']}

📱 POSTING STEPS:
1. Copy text above
2. Download image from GitHub
3. Create LinkedIn post with text + image
4. Engage with comments!

---
⏰ Auto-generated: {datetime.now().strftime('%H:%M %d-%m-%Y')}
🤖 Your LinkedIn automation working perfectly!"""

    else:
        telegram_message = f"""🚀 Fresh LinkedIn Content Ready!

📝 COPY THIS TO LINKEDIN:
{linkedin_content}

📸 Images: Check GitHub Actions artifacts
💡 Text-only posts work great too!

📱 POSTING STEPS:
1. Copy text above
2. Post to LinkedIn
3. Engage with your network!

---
⏰ Auto-generated: {datetime.now().strftime('%H:%M %d-%m-%Y')}
🤖 Your LinkedIn automation is working!"""
    
    # Send to Telegram
    print(f"\n📤 Sending LinkedIn content to Telegram...")
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': telegram_message
        }
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                print(f"✅ LinkedIn content sent to Telegram!")
                print(f"📱 Check your Telegram bot for the LinkedIn post!")
                
                # Also send image if available
                if image_info and os.path.exists(image_info['path']):
                    send_image_to_telegram(bot_token, chat_id, image_info['path'])
                
                return True
            else:
                print(f"❌ Telegram error: {result}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Send error: {str(e)}")
    
    return False

def send_image_to_telegram(bot_token, chat_id, image_path):
    """Send image to Telegram"""
    
    print(f"📸 Sending image to Telegram...")
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        
        with open(image_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': chat_id,
                'caption': '📸 LinkedIn post image - download and use with your post!'
            }
            
            response = requests.post(url, files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if result['ok']:
                    print(f"✅ Image sent to Telegram!")
                else:
                    print(f"⚠️ Image failed: {result}")
            else:
                print(f"⚠️ Image HTTP error: {response.status_code}")
                
    except Exception as e:
        print(f"⚠️ Image error: {str(e)}")

def main():
    """Main function"""
    
    print("🤖 Telegram LinkedIn Automation Test")
    print("=" * 45)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test bot setup
    if test_telegram_bot():
        print(f"\n🎉 Telegram setup is working perfectly!")
        
        # Send LinkedIn content
        if send_linkedin_content():
            print(f"\n🎊 SUCCESS! LinkedIn content delivered via Telegram!")
            print(f"📱 Your automation is now fully working!")
            print(f"🚀 You'll receive content 3x daily automatically!")
        else:
            print(f"\n⚠️ Content generation worked but delivery failed")
    else:
        print(f"\n❌ Telegram setup needs to be fixed")
        print(f"💡 Check your TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")

if __name__ == "__main__":
    main()