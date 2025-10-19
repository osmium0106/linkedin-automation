# 🚀 GitHub Actions Setup for Telegram Automation

This guide will help you set up GitHub Actions to automatically run your Telegram LinkedIn automation **3 times daily**.

## 📋 Prerequisites

1. ✅ Telegram bot is working (test with `python test_telegram_automation.py`)
2. ✅ GitHub repository is set up
3. ✅ You have your Telegram bot token and chat ID

## 🔐 Step 1: Configure GitHub Secrets

1. **Go to your GitHub repository**
2. **Click on Settings** (top menu)
3. **Navigate to Secrets and variables → Actions** (left sidebar)
4. **Click "New repository secret"**

Add these two secrets:

### Secret 1: TELEGRAM_BOT_TOKEN
- **Name**: `TELEGRAM_BOT_TOKEN`
- **Value**: `8286273163:AAH1sECsD-zE6YxfaYFZq6x5T5ifQUrEYxo`

### Secret 2: TELEGRAM_CHAT_ID  
- **Name**: `TELEGRAM_CHAT_ID`
- **Value**: `1874022460`

## ⏰ Step 2: Automation Schedule

Your automation is configured to run **3 times daily**:

| Time (UTC) | Time (IST) | Purpose |
|------------|------------|---------|
| 9:00 AM    | 2:30 PM    | Afternoon update |
| 2:00 PM    | 7:30 PM    | Evening update |
| 6:00 PM    | 11:30 PM   | Night update |

## 🔄 Step 3: Enable GitHub Actions

1. **Go to the Actions tab** in your repository
2. **Enable GitHub Actions** (if not already enabled)
3. **Commit and push** your changes to trigger the workflow

## 🧪 Step 4: Test the Setup

### Manual Test
1. Go to **Actions** tab in your repository
2. Click on **"Telegram LinkedIn Automation"** workflow
3. Click **"Run workflow"** button
4. Click **"Run workflow"** to start manual execution
5. Check your Telegram for the message!

### Check Scheduled Runs
- The workflow will automatically run at the scheduled times
- Check the **Actions** tab to see execution history
- Each run will show success/failure status

## 📊 Step 5: Monitor Your Automation

### GitHub Actions Dashboard
- Go to **Actions** tab to see all runs
- Click on any run to see detailed logs
- Green checkmark = successful run
- Red X = failed run (check logs for errors)

### Telegram Messages
You should receive **3 messages daily** with:
- 📰 Fresh tech news content
- 🎯 Professional LinkedIn post format
- 🖼️ Relevant images
- #️⃣ Hashtags and source links

## 🔧 Troubleshooting

### If automation isn't running:

1. **Check GitHub Secrets**
   ```
   Repository → Settings → Secrets and variables → Actions
   Verify: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set
   ```

2. **Check Workflow File**
   ```
   Verify: .github/workflows/telegram-linkedin-automation.yml exists
   Check: Cron schedule is correct
   ```

3. **Test Manually**
   ```bash
   # Run locally first
   python test_telegram_automation.py
   
   # Then test via GitHub Actions manual trigger
   ```

### If messages aren't being received:

1. **Verify Bot Token**
   - Check if bot token is correct in GitHub secrets
   - Test bot manually: send `/start` to your bot

2. **Verify Chat ID**
   - Message @userinfobot to confirm your chat ID
   - Update GitHub secret if needed

3. **Check Bot Permissions**
   - Ensure bot can send messages
   - Start a conversation with your bot first

## 📱 Step 6: Using the Content

When you receive Telegram messages:

1. **Copy the text** from Telegram message
2. **Download the image** (if included)
3. **Go to LinkedIn**:
   - Create new post
   - Paste the text
   - Add the downloaded image
   - Hit "Post"!

## ⚡ Quick Commands

```bash
# Test locally
python test_telegram_automation.py

# Check requirements
pip install -r requirements.txt

# View workflow status
# Go to: https://github.com/YOUR_USERNAME/linkedin-automation/actions
```

## 🎯 Expected Results

After setup, you'll receive **3 daily messages** like this:

```
🚀 Revolutionary AI Breakthrough Changes Everything

💡 Key takeaways:
• Significant advancement in machine learning capabilities
• Potential applications across multiple industries  
• Important implications for future technology development

This development could reshape how we approach AI integration. What are your thoughts on this breakthrough?

#AI #Technology #Innovation #MachineLearning #TechNews #LinkedIn

📖 Read more: https://techcrunch.com/article-link
📰 Source: TechCrunch
```

## ✅ Success Checklist

- [ ] GitHub secrets configured (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
- [ ] GitHub Actions enabled
- [ ] Workflow file exists (.github/workflows/telegram-linkedin-automation.yml)
- [ ] Manual test successful
- [ ] Receiving scheduled messages (wait 24 hours for first automatic run)
- [ ] Content quality looks good
- [ ] Ready to share on LinkedIn!

---

**🎉 Congratulations!** Your automation is now running on GitHub's servers, completely free, and will send you professional LinkedIn content 3 times daily to your Telegram! 

No more manual work - just copy, paste, and post to LinkedIn! 🚀