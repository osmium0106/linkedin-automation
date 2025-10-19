# 🤖 How to Get Telegram Bot Token from BotFather

## Step-by-Step Guide (Takes 3 minutes)

### 📱 Step 1: Open Telegram
- Open Telegram app on your phone or computer
- Or use web.telegram.org in your browser

### 🤖 Step 2: Find BotFather
1. **Search for**: `@BotFather`
2. **Or click this link**: https://t.me/botfather
3. **Start the conversation** by clicking "START"

### 💬 Step 3: Create Your Bot
**Type exactly this message:**
```
/newbot
```

**BotFather will ask for bot name. Type:**
```
LinkedIn Content Bot
```

**BotFather will ask for username. Type:**
```
your_linkedin_bot
```
*(Must end with 'bot' and be unique)*

### 🔑 Step 4: Get Your Token
**BotFather will reply with something like:**
```
Done! Congratulations on your new bot. You have a token:

1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ123456789

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**Copy this entire token:** `1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ123456789`

### 💬 Step 5: Get Your Chat ID
1. **Message your new bot** (click the link BotFather gives you)
2. **Send any message** to your bot like: `Hello`
3. **Open this URL** in browser (replace YOUR_TOKEN):
   ```
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
   ```
4. **Look for "chat":{"id":123456789}** - that number is your chat ID

### 📝 Step 6: Add to .env File
Add these lines to your `.env` file:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ123456789
TELEGRAM_CHAT_ID=123456789
```

---

## 🎯 Quick Example:

### What you type to BotFather:
```
/newbot
LinkedIn Content Bot
osmium_linkedin_bot
```

### What BotFather replies:
```
Done! Here's your token:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ123456789

Use this token to access the HTTP API:
https://core.telegram.org/bots/api
```

### Your .env file becomes:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ123456789
TELEGRAM_CHAT_ID=123456789
```

---

## 🔍 Finding Your Chat ID (Alternative Method):

If the URL method doesn't work:

1. **Add this bot**: @userinfobot
2. **Send**: `/start`
3. **It will reply with your chat ID**

---

## ✅ Testing Your Setup:

Once you have both token and chat ID, test with:
```bash
python telegram_linkedin_automation.py
```

You should receive a message in your Telegram bot chat!

---

## 🚨 Troubleshooting:

**Bot username taken?**
- Try: `your_name_linkedin_bot`
- Try: `linkedin_automation_bot_2025`

**Can't find chat ID?**
- Make sure you sent at least one message to your bot first
- Use @userinfobot as alternative method

**Token doesn't work?**
- Make sure you copied the entire token (including all characters)
- Don't include any spaces before/after

---

*Generated: 2025-10-20*
*This guide will get your Telegram automation working in 3 minutes!*