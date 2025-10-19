# 🤖 LinkedIn Automation Bot 

**100% Free AI-Powered LinkedIn Content Generator**

## 🛠️ Usage

### 🐳 Docker Commands

```bash
# Windows
docker-run.bat start     # Start the bot in scheduled mode
docker-run.bat auth      # Setup LinkedIn authentication  
docker-run.bat test      # Test all components
docker-run.bat post      # Create a single post now
docker-run.bat generate  # Generate content only
docker-run.bat logs      # View bot logs
docker-run.bat stop      # Stop the bot
docker-run.bat cleanup   # Clean up Docker resources

# Linux/Mac  
./docker-run.sh start    # Start the bot in scheduled mode
./docker-run.sh auth     # Setup LinkedIn authentication
./docker-run.sh test     # Test all components
./docker-run.sh post     # Create a single post now
./docker-run.sh generate # Generate content only
./docker-run.sh logs     # View bot logs
./docker-run.sh stop     # Stop the bot
./docker-run.sh cleanup  # Clean up Docker resources
```

### 🐍 Local Python Commands

```bash
python main.py test      # Test all components
python main.py post      # Create a single post now  
python main.py schedule  # Start scheduled posting
python main.py generate  # Generate content only
```lly fetches trending news, generates AI captions and images, and posts to LinkedIn twice daily using completely free tools and services.

## ✨ Features

- 📰 **News Fetching**: Gets trending news from Google News RSS feeds
- 🤖 **AI Caption Generation**: Uses Hugging Face transformers for LinkedIn-style posts  
- 🎨 **AI Image Generation**: Creates images with Stable Diffusion models
- 📤 **Automated Posting**: Posts to LinkedIn via official API
- ⏰ **Scheduled Automation**: Runs twice daily (10 AM & 5 PM) via GitHub Actions
- 🆓 **100% Free**: Uses only free tools and services

## 🚀 Quick Start

Choose your preferred setup method:

### 🐳 Docker Setup (Recommended)

```bash
git clone https://github.com/osmium0106/linkedin-automation.git
cd linkedin-automation

# Windows
docker-run.bat help

# Linux/Mac
chmod +x docker-run.sh
./docker-run.sh help
```

### 🐍 Local Python Setup

```bash
git clone https://github.com/osmium0106/linkedin-automation.git
cd linkedin-automation
pip install -r requirements.txt
```

### 2️⃣ LinkedIn App Setup

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Create a new app with these settings:
   - **Products**: Sign In with LinkedIn, Share on LinkedIn  
   - **Redirect URI**: `http://localhost:8000/callback`
   - **Scopes**: `r_liteprofile`, `r_emailaddress`, `w_member_social`

### 3️⃣ Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials:
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8000/callback
LINKEDIN_ACCESS_TOKEN=your_access_token_here
HUGGINGFACE_TOKEN=your_hf_token_here  # Optional
```

### 4️⃣ Authentication

```bash
# Run the authentication helper
python setup_auth.py
```

This will:
- Open LinkedIn OAuth in your browser
- Handle the callback automatically  
- Display your access token to add to `.env`

### 5️⃣ Test the Bot

```bash
# Test all components
python main.py test

# Generate content without posting
python main.py generate

# Create a single post
python main.py post
```

## 🛠️ Usage

### Local Commands

```bash
python main.py test      # Test all components
python main.py post      # Create a single post now  
python main.py schedule  # Start scheduled posting
python main.py generate  # Generate content only
```

### GitHub Actions Automation

1. **Add Repository Secrets**:
   - Go to Settings → Secrets and Variables → Actions
   - Add these secrets:
     - `LINKEDIN_CLIENT_ID`
     - `LINKEDIN_CLIENT_SECRET` 
     - `LINKEDIN_ACCESS_TOKEN`
     - `LINKEDIN_REDIRECT_URI`
     - `HUGGINGFACE_TOKEN` (optional)

2. **Automatic Schedule**: Posts automatically at 10 AM and 5 PM UTC daily

3. **Manual Trigger**: Use "Run workflow" button in Actions tab

## 📁 Project Structure

```
linkedin-automation/
├── main.py                 # Main orchestration script
├── config.py               # Configuration management
├── news_fetcher.py         # Google News RSS fetching
├── caption_generator.py    # AI caption generation
├── image_generator.py      # AI image creation
├── linkedin_poster.py      # LinkedIn API integration
├── setup_auth.py           # OAuth authentication helper
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .github/workflows/     # GitHub Actions automation
└── README.md              # This file
```

## 🧩 How It Works

### Step 1 — Fetch News Data 📰
- Uses Google News RSS feeds for trending topics
- Covers: Technology, AI, Business, Startups, Programming
- Selects random articles for variety

### Step 2 — Generate Captions 🤖  
- Uses Hugging Face BART model for summarization
- Creates LinkedIn-style posts with hashtags
- Includes engagement questions and call-to-actions

### Step 3 — Create AI Images 🎨
- Uses Stable Diffusion for image generation
- Topic-specific visual styles
- Fallback to text-based images if AI fails

### Step 4 — Post to LinkedIn 📤
- Official LinkedIn UGC Post API
- Supports text + image posts
- Automatic error handling and retries

### Step 5 — Schedule Automatically ⏰
- GitHub Actions runs twice daily
- No server costs - completely free
- Logs and artifacts for debugging

## 🔧 Configuration

### News Topics
Edit `Config.NEWS_TOPICS` in `config.py`:
```python
NEWS_TOPICS = [
    'technology',
    'artificial intelligence', 
    'business',
    'startups',
    'programming'
]
```

### Posting Schedule  
Edit `Config.POSTING_TIMES` in `config.py`:
```python
POSTING_TIMES = ['10:00', '17:00']  # 24-hour format
```

### AI Models
- **Caption**: `facebook/bart-large-cnn` (summarization)
- **Images**: `runwayml/stable-diffusion-v1-5` 
- Configurable in `config.py`

## 📊 Monitoring

### Logs
- `logs/linkedin_bot_YYYY-MM-DD.log` - Daily logs
- `logs/linkedin_bot_errors_YYYY-MM-DD.log` - Error logs
- GitHub Actions artifacts for automated runs

### Generated Content
- `generated_images/` - All created images
- Automatic cleanup after posting

## 🚨 Troubleshooting

### Common Issues

**"Import could not be resolved" errors**: 
```bash
pip install -r requirements.txt
```

**LinkedIn authentication fails**:
- Verify redirect URI matches exactly
- Check app has correct products enabled
- Ensure scopes are: `r_liteprofile r_emailaddress w_member_social`

**AI models won't load**:
- Check internet connection
- Verify Hugging Face token (if using gated models)
- GPU memory issues - fallback to CPU automatically

**GitHub Actions fails**:
- Verify all secrets are set correctly
- Check repository secrets match `.env` variables

### Getting Help

1. Check the logs for detailed error messages
2. Run `python main.py test` to diagnose issues
3. Open an issue with error logs and setup details

## 📝 License

MIT License - feel free to modify and use for your projects!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes  
4. Test thoroughly
5. Submit a pull request

## ⭐ Support

If this project helps you, please give it a star! ⭐

For questions or support, open an issue or reach out on LinkedIn.
