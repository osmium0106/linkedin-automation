# 🤖 Telegram LinkedIn Content Automation

An intelligent automation bot that fetches trending tech news, generates AI-powered LinkedIn content, and **automatically delivers it to your Telegram** for easy sharing on LinkedIn.

## ✨ Features

- 📰 **Smart News Fetching**: Automatically fetches trending tech news from multiple RSS feeds
- 🤖 **AI Content Generation**: Creates engaging LinkedIn posts with professional captions
- 🎨 **Image Integration**: Includes relevant images with each post
- 📱 **Telegram Delivery**: Automatically sends content to your Telegram for easy LinkedIn sharing
- ⏰ **Scheduled Automation**: Runs 3x daily via GitHub Actions (2:30 PM, 7:30 PM, 11:30 PM IST)
- 🔄 **Zero Maintenance**: Fully automated workflow requiring no manual intervention

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd linkedin-automation

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Telegram Bot Setup

1. **Create a Telegram Bot**:
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Choose a name and username for your bot
   - Save the bot token

2. **Get Your Chat ID**:
   - Start a chat with your new bot
   - Send any message
   - Message @userinfobot to get your chat ID

3. **Configure Environment**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your Telegram credentials
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

### 3. Test the Bot

```bash
# Test Telegram integration
python test_telegram_automation.py
```

## 📋 How It Works

1. **News Fetching**: Bot scans tech news from TechCrunch, Wired, and Ars Technica RSS feeds
2. **Content Creation**: Generates professional LinkedIn posts with:
   - Engaging headlines
   - Key takeaways
   - Relevant hashtags
   - Professional formatting
3. **Image Selection**: Includes relevant images from news articles
4. **Telegram Delivery**: Sends complete post with image to your Telegram bot
5. **Easy Sharing**: Copy content from Telegram and share on LinkedIn

## 🔄 Automation Schedule

The bot runs automatically **3 times per day** via GitHub Actions:
- **2:30 PM IST** - Afternoon update
- **7:30 PM IST** - Evening update  
- **11:30 PM IST** - Night update

No manual intervention required!

## 📱 Using the Content

1. **Receive in Telegram**: Bot sends you the complete post with image
2. **Copy Text**: Select and copy the formatted text from Telegram
3. **Share on LinkedIn**: 
   - Open LinkedIn mobile app or website
   - Create new post
   - Paste the text
   - Add the image (download from Telegram)
   - Post to your network!

## 📂 File Structure

```
linkedin-automation/
├── test_telegram_automation.py    # Main automation script
├── news_fetcher.py               # News RSS feed handler
├── .env                         # Environment variables
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
├── .github/workflows/           # GitHub Actions automation
├── generated_images/            # Downloaded images
└── docs/                       # Setup guides
```

## 🛠️ Technical Details

### Dependencies
- **requests**: HTTP requests and Telegram API
- **feedparser**: RSS feed parsing
- **python-dotenv**: Environment variable management

### News Sources
- TechCrunch RSS Feed
- Wired Technology RSS Feed  
- Ars Technica RSS Feed

### Content Format
Each post includes:
- **Headline**: Eye-catching title
- **Summary**: 2-3 key takeaways
- **Call to Action**: Engagement question
- **Hashtags**: Relevant tech hashtags
- **Source Attribution**: Original article link
- **Image**: Relevant visual content

## 🔧 Configuration Options

### Environment Variables (.env)
```bash
# Required
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Optional (defaults provided)
NEWS_TOPICS=technology,artificial intelligence,business
POSTING_TIMES=10:00,17:00
MAX_CAPTION_LENGTH=1300
```

## 🚨 Troubleshooting

### Common Issues

**Bot Not Responding**
- Verify bot token is correct
- Ensure chat ID is accurate
- Check bot permissions

**No News Content**
- Check internet connection
- Verify RSS feeds are accessible
- Check news_fetcher.py logs

**GitHub Actions Not Running**
- Verify repository secrets are set
- Check workflow file syntax
- Ensure GitHub Actions are enabled

## 📊 Example Output

### Telegram Message Format
```
🚀 OpenAI Announces GPT-5 with Revolutionary Capabilities

💡 Key takeaways:
• Breakthrough advances in AI reasoning capabilities
• Enhanced safety measures and alignment features  
• Potential impact across multiple industry sectors

This development represents a significant milestone in AI evolution. What are your thoughts on the future implications?

#AI #Technology #Innovation #OpenAI #MachineLearning #ArtificialIntelligence

📖 Read more: https://techcrunch.com/article-link
📰 Source: TechCrunch
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Telegram Bot API** for reliable message delivery
- **RSS Feed providers** for news content
- **GitHub Actions** for free automation hosting
- **Open source community** for tools and libraries

---

**🚀 Ready to automate your LinkedIn content? Set up your Telegram bot and let the automation begin!**