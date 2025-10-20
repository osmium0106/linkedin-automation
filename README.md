# 🤖 Enhanced LinkedIn Automation

Automated LinkedIn content delivery via Telegram with AI-generated images, smart prompting, and professional branding.

## ✨ Features

- 🔄 **Fresh News Detection** - No duplicate articles, 7-day memory
- 🤖 **AI-Powered Prompts** - Gemini AI generates creative image prompts  
- 🎨 **High-Quality Images** - FLUX.1-schnell with 90+ second generation
- 🏷️ **Professional Branding** - Automatic logo overlay
- 📰 **Title Overlays** - News titles professionally displayed on images
- 📱 **Clean Formatting** - Bullet points, "Read More" links, hashtags
- ⏰ **Scheduled Delivery** - 3x daily automated posts

## 🚀 Quick Start

1. **Clone & Setup**:
   ```bash
   git clone https://github.com/osmium0106/linkedin-automation.git
   cd linkedin-automation
   ```

2. **Add GitHub Secrets**:
   - `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
   - `TELEGRAM_CHAT_ID` - Your Telegram chat ID  
   - `HUGGINGFACE_TOKEN` - Hugging Face API token
   - `GEMINI_API_KEY` - Google Gemini API key

3. **Deploy**:
   ```bash
   git push origin main
   ```

## ⏰ Schedule

Automatically delivers content at:
- **9:00 AM IST** (3:30 AM UTC)
- **12:00 PM IST** (6:30 AM UTC)
- **4:00 PM IST** (10:30 AM UTC)

## 📱 Sample Output

**Message Format:**
```
🚀 AI Breakthrough in Medical Diagnosis

💡 Key Insights:
• Revolutionary machine learning advancement
• 95% accuracy in early disease detection  
• Potential to transform healthcare industry

🔍 Why This Matters:
• Stay ahead of industry trends
• Leverage cutting-edge developments
• Make informed business decisions

📊 Topic Focus: #ArtificialIntelligence

What are your thoughts on this development?

Read More: [original_article_link]

---
🤖 Powered by AI | Fresh insights delivered daily

#TechNews #Innovation #Business #AI #Technology
```

**Image Features:**
- AI-generated visualization based on news content
- ThinkersKlub logo in top-right corner
- News title overlay at bottom with professional styling

## 🛠️ Technical Stack

- **Content**: RSS feeds from multiple tech sources
- **AI Images**: Hugging Face FLUX.1-schnell model
- **Prompts**: Google Gemini AI for creative generation
- **Branding**: PIL/Pillow for logo and title overlays  
- **Delivery**: Telegram Bot API
- **Automation**: GitHub Actions with cron scheduling
- **Storage**: JSON-based article tracking

## 📊 System Specifications

- **Generation Time**: 60-90 seconds per image (premium quality)
- **Inference Steps**: 12 steps for maximum detail
- **Duplicate Prevention**: 7-day article memory
- **Fallback System**: Enhanced prompts when Gemini unavailable
- **Success Rate**: 3 retries with extended wait times

## 🎯 Content Sources

- Technology news and breakthroughs
- Artificial Intelligence developments  
- Robotics and automation
- Programming and software
- Business and startup news

## 🔧 Maintenance

The system is fully automated and requires no maintenance:
- ✅ Self-healing with fallback systems
- ✅ Automatic duplicate detection
- ✅ Smart error handling and retries
- ✅ Quality monitoring and optimization

---

**🚀 Deploy once, enjoy fresh LinkedIn content 3x daily!**