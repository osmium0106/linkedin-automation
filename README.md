# 🤖 LinkedIn Automation Bot

An intelligent LinkedIn automation bot that fetches trending news, generates AI-powered content, and **automatically posts to LinkedIn** using multiple fallback strategies.

## ✨ Features

- 📰 **Smart News Fetching**: Automatically fetches trending news from Google News across multiple topics
- 🤖 **AI Content Generation**: Uses BART AI model to create engaging LinkedIn posts with professional captions
- 🎨 **AI Image Generation**: Creates relevant images using Stable Diffusion AI
- � **Automatic Posting**: Posts directly to LinkedIn using multiple fallback strategies (API + Browser Automation)
- 🌐 **Browser Automation**: Selenium-powered fallback for reliable posting when API limits are reached
- � **Smart Content Management**: Organized content storage with posting guides as backup
- 📊 **Content Analytics**: Tracks generated content with summaries and organization

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

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials (optional - only needed for direct API posting)
```

### 3. Usage

```bash
# Generate content (recommended)
python main.py generate

# Generate and prepare for posting
python main.py post

# View content summary
python main.py summary

# Open posting folder
python main.py open

# Test all components
python main.py test
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python main.py generate` | Generate content only (no posting prep) |
| `python main.py post` | Generate content and prepare for posting |
| `python main.py summary` | Show content ready for posting |
| `python main.py open` | Open the posting folder |
| `python main.py test` | Test all components |
| `python main.py schedule` | Start scheduled posting (advanced) |

## 📂 Content Organization

Generated content is organized in the `ready_to_post/` folder:

```
ready_to_post/
├── news_automation/
│   ├── post_20241020_123456.txt          # Post content
│   ├── post_20241020_123456_image.jpg    # Generated image
│   └── posting_guide_20241020_123456.md  # Posting instructions
└── tech_news/
    └── ...
```

Each post includes:
- ✅ **Formatted text content** ready to copy/paste
- ✅ **Generated image** optimized for LinkedIn
- ✅ **Posting guide** with step-by-step instructions
- ✅ **Quick share URL** for one-click posting
- ✅ **Analytics** (character count, hashtags, etc.)

## 🔗 Easy Posting Methods

### Method 1: Quick Share URL (Fastest)
1. Check the posting guide file
2. Click the "Quick Share URL"
3. Review and post on LinkedIn

### Method 2: Copy & Paste
1. Open the `.txt` file
2. Copy the content between the `---` markers
3. Go to LinkedIn.com
4. Paste and add the image

### Method 3: Mobile App (Best for Images)
1. Transfer image to your phone
2. Open LinkedIn mobile app
3. Create new post with the image
4. Copy/paste the text content

## 🛠️ Technical Details

### AI Models Used
- **Text Generation**: Facebook BART-large-CNN (1.6GB)
- **Image Generation**: Stable Diffusion v1.5 (3.4GB)
- **News Source**: Google News RSS feeds

### System Requirements
- Python 3.8+
- 8GB RAM (recommended for AI models)
- 5GB+ disk space (for AI models)
- Internet connection

### Performance
- **Content Generation**: ~30-60 seconds
- **News Fetching**: ~5-10 seconds
- **AI Caption**: ~5-15 seconds
- **AI Image**: ~20-40 seconds (CPU)

## 🔧 Configuration Options

### News Topics (configurable in `config.py`)
- Technology
- Artificial Intelligence  
- Business
- Startups
- Programming
- LinkedIn

### AI Settings
- Image dimensions: 1200x627 (LinkedIn optimized)
- Caption length: 500-1500 characters
- Hashtag generation: Automatic
- Content style: Professional/engaging

## 📊 Content Analytics

The bot tracks:
- Total posts generated
- Posts by topic category
- Character counts
- Hashtag analysis
- Generation timestamps
- Success/failure rates

## 🚨 Important Notes

### LinkedIn API Limitations
- Direct API posting requires LinkedIn Partner Program access
- Current implementation focuses on content generation + easy manual posting
- API authentication code included for future use

### Content Quality
- All content is AI-generated and should be reviewed before posting
- Images are created by AI and may need customization
- News articles are automatically selected - relevance may vary

## 🐛 Troubleshooting

### Common Issues

**Model Loading Errors**
```bash
# Clear model cache
rm -rf ~/.cache/huggingface/

# Reinstall transformers
pip uninstall transformers
pip install transformers
```

**Image Generation Errors**
- The bot automatically creates fallback images if AI generation fails
- Check `logs/` folder for detailed error messages

**News Fetching Issues**
- Some topics may have URL encoding issues (automatically handled)
- Internet connection required for news fetching

## 📝 Example Output

### Generated Content Example
```
🚀 OpenAI Announces GPT-5 with Revolutionary Capabilities - TechCrunch

💡 Key takeaways:
• Demonstrates breakthrough advances in AI technology
• Shows potential for reshaping multiple industries
• Highlights importance of responsible AI development

What are your thoughts on this AI advancement?

#AI #Technology #Innovation #OpenAI #GPT5 #MachineLearning

📖 Read more: [article link]
📰 Source: TechCrunch
```

## 🔄 Automation Workflows

### Daily Content Generation
```bash
# Morning routine
python main.py post
python main.py summary

# Review and post manually to LinkedIn
```

### Weekly Content Planning
```bash
# Generate multiple posts
for i in {1..5}; do
    python main.py generate
    sleep 10
done

# Review all content
python main.py summary
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for AI models
- **Google News** for news feeds  
- **LinkedIn** for the platform
- **Open source community** for tools and libraries

---

**🚀 Ready to automate your LinkedIn content? Start with `python main.py post`!**