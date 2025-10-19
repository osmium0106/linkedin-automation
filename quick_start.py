#!/usr/bin/env python3
"""
Quick Start Script for GitHub Actions LinkedIn Automation
Run this after setting up your GitHub repository
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    print("🚀 LinkedIn Automation - Quick GitHub Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Please run this script from the linkedin-automation directory")
        sys.exit(1)
    
    print("This script will help you push your code to GitHub")
    print("Make sure you have:")
    print("✅ Created a GitHub repository")
    print("✅ Have your GitHub username ready")
    print()
    
    # Get GitHub username and repo name
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("❌ GitHub username is required")
        sys.exit(1)
    
    repo_name = input("Enter repository name (default: linkedin-automation): ").strip()
    if not repo_name:
        repo_name = "linkedin-automation"
    
    print(f"\n📋 Setup Summary:")
    print(f"   GitHub Username: {username}")
    print(f"   Repository Name: {repo_name}")
    print(f"   Repository URL: https://github.com/{username}/{repo_name}")
    
    confirm = input("\nProceed with setup? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Setup cancelled")
        sys.exit(0)
    
    print(f"\n🚀 Setting up GitHub repository...")
    
    # Commands to run
    commands = [
        ("git add .", "Adding files to git"),
        ("git commit -m \"Initial LinkedIn automation setup\"", "Committing changes"),
        (f"git remote add origin https://github.com/{username}/{repo_name}.git", "Adding GitHub remote"),
        ("git push -u origin main", "Pushing to GitHub")
    ]
    
    # Execute commands
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n⚠️ Command failed: {command}")
            print("You may need to run this manually")
            continue
    
    print(f"\n🎉 GitHub setup completed!")
    print(f"📍 Repository URL: https://github.com/{username}/{repo_name}")
    
    print(f"\n🔐 IMPORTANT: Set up GitHub Secrets")
    print("=" * 40)
    print(f"1. Go to: https://github.com/{username}/{repo_name}/settings/secrets/actions")
    print(f"2. Click 'New repository secret'")
    print(f"3. Add these secrets:")
    
    # Read current .env to show what secrets to add
    secrets_to_add = []
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key = line.split('=')[0].strip()
                    if key in ['LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_CLIENT_ID', 'LINKEDIN_CLIENT_SECRET', 'HUGGINGFACE_API_KEY']:
                        secrets_to_add.append(key)
    
    for secret in secrets_to_add:
        print(f"   • {secret}")
    
    print(f"\n📅 Automation Schedule (UTC):")
    print(f"   • 9:00 AM UTC (Morning post)")
    print(f"   • 2:00 PM UTC (Afternoon post)")  
    print(f"   • 6:00 PM UTC (Evening post)")
    
    print(f"\n🧪 Test Your Setup:")
    print(f"1. Go to: https://github.com/{username}/{repo_name}/actions")
    print(f"2. Click 'LinkedIn Auto Post' workflow")
    print(f"3. Click 'Run workflow' → 'Run workflow'")
    print(f"4. Monitor the execution")
    
    print(f"\n📚 More Help:")
    print(f"• Read GITHUB_ACTIONS_SETUP.md for detailed instructions")
    print(f"• Check Actions tab for execution logs")
    print(f"• Monitor your LinkedIn for automated posts")
    
    print(f"\n✨ Your LinkedIn automation is now ready to run on autopilot!")

if __name__ == "__main__":
    main()