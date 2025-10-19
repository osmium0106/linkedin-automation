# GitHub Actions Setup Guide for LinkedIn Automation

This guide will help you set up your LinkedIn automation to run automatically via GitHub Actions on a schedule.

## 🚀 Quick Setup

### 1. Push Your Code to GitHub

First, push your LinkedIn automation code to a GitHub repository:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial LinkedIn automation bot"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/linkedin-automation.git

# Push to GitHub
git push -u origin main
```

### 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and Variables → Actions

Add the following secrets:

#### Required Secrets:
- `LINKEDIN_ACCESS_TOKEN` - Your LinkedIn API access token
- `LINKEDIN_CLIENT_ID` - Your LinkedIn app client ID  
- `LINKEDIN_CLIENT_SECRET` - Your LinkedIn app client secret

#### Optional Secrets:
- `HUGGINGFACE_API_KEY` - Your HuggingFace API key (for AI models)

### 3. Configure Schedule (Optional)

Edit `.github/workflows/linkedin-automation.yml` to customize posting times:

```yaml
schedule:
  # Run at 9:00 AM UTC (4:00 AM EST)
  - cron: '0 9 * * *'
  # Run at 2:00 PM UTC (9:00 AM EST)  
  - cron: '0 14 * * *'
  # Run at 6:00 PM UTC (1:00 PM EST)
  - cron: '0 18 * * *'
```

**Cron Format:** `minute hour day_of_month month day_of_week`
- `0 9 * * *` = Every day at 9:00 AM UTC
- `0 */6 * * *` = Every 6 hours
- `0 9 * * 1-5` = Every weekday at 9:00 AM UTC

### 4. Test Your Setup

#### Manual Test:
1. Go to Actions tab in your GitHub repository
2. Click "LinkedIn Automation Bot" workflow
3. Click "Run workflow" button
4. Click "Run workflow" to execute immediately

#### Check Logs:
- View execution logs in the Actions tab
- Download artifacts containing execution logs and generated content

## 🔧 Configuration Options

### Environment Variables (in GitHub Secrets)

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn API access token | ✅ Yes |
| `LINKEDIN_CLIENT_ID` | LinkedIn app client ID | ✅ Yes |
| `LINKEDIN_CLIENT_SECRET` | LinkedIn app client secret | ✅ Yes |
| `HUGGINGFACE_API_KEY` | HuggingFace API for AI models | ❌ Optional |

### Schedule Configuration

The automation runs on these default times (UTC):
- **9:00 AM UTC** - Morning post
- **2:00 PM UTC** - Afternoon post  
- **6:00 PM UTC** - Evening post

**Convert to your timezone:**
- UTC+0 (London): Same times
- UTC-5 (EST): 4:00 AM, 9:00 AM, 1:00 PM
- UTC-8 (PST): 1:00 AM, 6:00 AM, 10:00 AM
- UTC+1 (Paris): 10:00 AM, 3:00 PM, 7:00 PM

## 📊 Monitoring & Logs

### GitHub Actions Dashboard
- Go to **Actions** tab in your repository
- View all workflow runs
- Check success/failure status
- Download execution logs

### Artifacts
Each run generates artifacts containing:
- Execution logs (JSON format)
- Generated content files
- Error logs (if any)

### Notifications
Configure GitHub to send you email notifications:
1. Go to GitHub Settings → Notifications
2. Enable "Actions" notifications
3. Choose email frequency

## 🛠️ Troubleshooting

### Common Issues:

#### 1. "Missing required secrets"
**Solution:** Add all required secrets in repository settings

#### 2. "LinkedIn API errors" 
**Solution:** 
- Verify your LinkedIn app permissions
- Check if access token is valid
- Ensure app has posting permissions

#### 3. "Workflow doesn't run"
**Solution:**
- Check cron syntax
- Ensure repository is not private (free accounts have limits)
- Verify workflow file is in correct path

#### 4. "Dependencies installation fails"
**Solution:**
- Check `requirements.txt` format
- Verify all packages are available on PyPI
- Consider using lighter package versions

### Debug Mode
Add this to your workflow for debugging:

```yaml
- name: 🐛 Debug Environment
  run: |
    echo "Python version: $(python --version)"
    echo "Pip version: $(pip --version)"
    echo "Current directory: $(pwd)"
    echo "Files: $(ls -la)"
    echo "Environment variables:"
    env | grep -E "(GITHUB_|LINKEDIN_)" | sort
```

## 💡 Pro Tips

### 1. Test Locally First
Before pushing to GitHub, test your automation locally:
```bash
python github_runner.py
```

### 2. Use Manual Triggers
The workflow includes manual trigger option for testing:
- Go to Actions → LinkedIn Automation Bot
- Click "Run workflow"
- Test without waiting for scheduled time

### 3. Monitor Rate Limits
- LinkedIn API has rate limits
- Space out your posts appropriately
- Monitor for 429 (rate limit) errors

### 4. Backup Strategy
- Keep local copies of your content
- Use git branches for experiments
- Regular backups of your `.env` file (locally only)

## 🔐 Security Best Practices

### 1. Never Commit Secrets
- Use GitHub Secrets only
- Add `.env` to `.gitignore`
- Never hardcode API keys

### 2. Minimal Permissions
- Use LinkedIn app with minimal required permissions
- Regularly rotate access tokens
- Monitor app usage in LinkedIn developer console

### 3. Repository Security
- Keep repository private if possible
- Use branch protection rules
- Enable security alerts

## 📅 Scheduling Examples

```yaml
# Every day at 9 AM UTC
- cron: '0 9 * * *'

# Every weekday at 2 PM UTC  
- cron: '0 14 * * 1-5'

# Every 6 hours
- cron: '0 */6 * * *'

# Monday, Wednesday, Friday at 10 AM UTC
- cron: '0 10 * * 1,3,5'

# First day of every month at 8 AM UTC
- cron: '0 8 1 * *'
```

## 🎯 Next Steps

After setup:

1. **Monitor First Few Runs**
   - Check Actions tab for successful execution
   - Verify posts appear on LinkedIn
   - Review generated content quality

2. **Optimize Content**
   - Adjust content generation parameters
   - Fine-tune posting topics
   - Monitor engagement metrics

3. **Scale Up**
   - Add more posting times
   - Implement content variations
   - Add image generation

4. **Maintenance**
   - Regular token renewal
   - Update dependencies
   - Monitor API changes

## ❓ Support

If you encounter issues:

1. Check GitHub Actions logs
2. Review LinkedIn developer console
3. Test locally with same environment
4. Check API documentation updates

**Happy Automating!** 🤖✨