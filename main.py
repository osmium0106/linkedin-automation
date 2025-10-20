#!/usr/bin/env python3
"""
Enhanced Telegram LinkedIn Content Automation
Main entry point for automated LinkedIn content delivery via Telegram
"""

import os
import sys
from datetime import datetime

def main():
    """Run the enhanced LinkedIn content automation"""
    try:
        # Load environment variables (works locally, GitHub Actions uses secrets)
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass  # dotenv not available in GitHub Actions, that's fine
        
        print("🤖 Starting LinkedIn Content Automation")
        print("=" * 50)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
        print("🚀 Features: Fresh news • AI prompts • Logo branding • Title overlays")
        
        # Import and run the enhanced automation
        from news_image_generator import NewsImageGenerator
        
        # Generate and deliver content
        image_generator = NewsImageGenerator()
        result = image_generator.generate_image_for_fresh_news()
        
        if result:
            article = result['article']
            image_path = result['image_path']
            is_fallback = result.get('fallback', False)
            
            print(f"✅ Content generated successfully!")
            print(f"📰 Article: {article['title'][:60]}...")
            print(f"🖼️ Image: {image_path}")
            
            # Send to Telegram
            success = send_to_telegram(article, image_path)
            
            if success:
                print("🎊 SUCCESS! LinkedIn content delivered via Telegram!")
                print("📱 Check your Telegram bot for the latest post!")
                return 0
            else:
                print("❌ Failed to send to Telegram")
                return 1
        else:
            print("❌ Failed to generate content")
            return 1
            
    except Exception as e:
        print(f"❌ Error in automation: {e}")
        import traceback
        traceback.print_exc()
        return 1

def send_to_telegram(article, image_path):
    """Send content and image to Telegram"""
    try:
        import requests
        from dotenv import load_dotenv
        
        load_dotenv()
        
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            print("❌ Missing Telegram credentials")
            return False
        
        # Create LinkedIn content
        description = article['description'][:300] if article['description'] else "Breaking news in the tech industry"
        
        # Create bullet points from description
        sentences = description.split('. ')[:3]
        bullet_points = []
        for sentence in sentences:
            if sentence.strip() and len(sentence.strip()) > 10:
                clean_sentence = sentence.strip().rstrip('.')
                if len(clean_sentence) > 80:
                    clean_sentence = clean_sentence[:80] + "..."
                bullet_points.append(f"• {clean_sentence}")
        
        # Fallback bullet points if description is poor
        if len(bullet_points) < 2:
            topic_insights = {
                'technology': ["Latest technological breakthrough", "Impact on digital transformation", "Future industry implications"],
                'artificial intelligence': ["AI advancement with real-world applications", "Machine learning innovation", "Potential business transformation"],
                'robotics': ["Automation technology progress", "Manufacturing and industry impact", "Future of human-robot collaboration"],
                'programming': ["Software development innovation", "Developer productivity enhancement", "Programming language evolution"],
                'business': ["Market dynamics and trends", "Strategic business implications", "Economic impact analysis"],
                'startups': ["Entrepreneurial innovation", "Investment and funding trends", "Startup ecosystem growth"]
            }
            fallback_points = topic_insights.get(article['topic'].lower(), ["Industry development", "Market innovation", "Technology advancement"])
            bullet_points = [f"• {point}" for point in fallback_points[:3]]
        
        linkedin_content = f"""🚀 **{article['title']}**

💡 **Key Insights:**
{chr(10).join(bullet_points)}

🔍 **Why This Matters:**
• Stay ahead of industry trends
• Leverage cutting-edge developments  
• Make informed business decisions

📊 **Topic Focus:** #{article['topic'].replace(' ', '').title()}

What are your thoughts on this development? How do you see this impacting the industry? Share your insights below! 👇

**Read More:** {article['link']}

---
🤖 *Powered by AI | Fresh insights delivered daily*

#TechNews #Innovation #Business #AI #Technology #Startups"""

        # Send text content
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': linkedin_content,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(telegram_url, json=payload)
        
        if response.status_code == 200:
            result_msg = response.json()
            if result_msg['ok']:
                print(f"✅ LinkedIn content sent to Telegram!")
                
                # Send image if available
                if image_path and os.path.exists(image_path):
                    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
                    
                    with open(image_path, 'rb') as photo:
                        files = {'photo': photo}
                        data = {
                            'chat_id': chat_id,
                            'caption': f"🎨 AI-Generated visualization for: {article['title'][:100]}..."
                        }
                        
                        response = requests.post(telegram_url, files=files, data=data)
                        
                        if response.status_code == 200:
                            result_img = response.json()
                            if result_img['ok']:
                                print(f"✅ Image sent to Telegram!")
                                return True
                            else:
                                print(f"⚠️ Error sending image: {result_img}")
                        else:
                            print(f"⚠️ HTTP error sending image: {response.status_code}")
                
                return True
            else:
                print(f"❌ Error sending text: {result_msg}")
                return False
        else:
            print(f"❌ HTTP error sending text: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending to Telegram: {e}")
        return False

if __name__ == "__main__":
    exit(main())