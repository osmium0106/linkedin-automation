#!/usr/bin/env python3
"""
GitHub Repository Setup Helper
Helps prepare your LinkedIn automation for GitHub Actions deployment
"""

import os
import subprocess
import sys
from pathlib import Path

def check_git_status():
    """Check if git is initialized and configured"""
    print("🔍 Checking Git status...")
    
    # Check if git is installed
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Git is not installed or not in PATH")
            return False
        print(f"✅ {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Git is not installed")
        return False
    
    # Check if git repo is initialized
    if not Path('.git').exists():
        print("⚠️ Git repository not initialized")
        return False
    
    print("✅ Git repository initialized")
    return True

def check_required_files():
    """Check if all required files exist"""
    print("\n📋 Checking required files...")
    
    required_files = [
        'main.py',
        'config.py', 
        '.env',
        'requirements.txt',
        '.github/workflows/linkedin-automation.yml',
        'github_runner.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def check_env_variables():
    """Check if environment variables are set"""
    print("\n🔐 Checking environment variables...")
    
    required_vars = [
        'LINKEDIN_ACCESS_TOKEN',
        'LINKEDIN_CLIENT_ID',
        'LINKEDIN_CLIENT_SECRET'
    ]
    
    # Load .env file
    env_file = Path('.env')
    env_vars = {}
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    
    missing_vars = []
    for var in required_vars:
        if var in env_vars and env_vars[var].strip():
            print(f"✅ {var}")
        else:
            print(f"❌ {var} (missing or empty)")
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars

def create_gitignore():
    """Create or update .gitignore file"""
    print("\n📝 Setting up .gitignore...")
    
    gitignore_content = """# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Generated content
linkedin_post_*.txt
generated_images/
*.jpg
*.png
*.jpeg

# Model cache
models/
.cache/

# OS
.DS_Store
Thumbs.db

# Temporary files
temp/
tmp/
"""
    
    try:
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✅ .gitignore created/updated")
        return True
    except Exception as e:
        print(f"❌ Error creating .gitignore: {str(e)}")
        return False

def git_setup_commands():
    """Display git setup commands"""
    print(f"\n🚀 Git Setup Commands")
    print("=" * 40)
    
    print("1. Add all files to git:")
    print("   git add .")
    
    print("\n2. Commit your changes:")
    print("   git commit -m \"Initial LinkedIn automation setup\"")
    
    print("\n3. Create GitHub repository (if not exists):")
    print("   - Go to https://github.com/new")
    print("   - Create repository named 'linkedin-automation'")
    print("   - Don't initialize with README (you have one)")
    
    print("\n4. Add GitHub remote:")
    print("   git remote add origin https://github.com/YOURUSERNAME/linkedin-automation.git")
    
    print("\n5. Push to GitHub:")
    print("   git push -u origin main")
    
    print("\n6. Set up GitHub Secrets:")
    print("   - Go to your repo → Settings → Secrets and Variables → Actions")
    print("   - Add these secrets:")
    print("     • LINKEDIN_ACCESS_TOKEN")
    print("     • LINKEDIN_CLIENT_ID") 
    print("     • LINKEDIN_CLIENT_SECRET")
    print("     • HUGGINGFACE_API_KEY (optional)")

def main():
    """Main setup function"""
    print("🤖 LinkedIn Automation - GitHub Actions Setup")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check git status
    git_ok = check_git_status()
    
    # Check required files
    files_ok, missing_files = check_required_files()
    
    # Check environment variables
    env_ok, missing_vars = check_env_variables()
    
    # Create .gitignore
    gitignore_ok = create_gitignore()
    
    # Summary
    print(f"\n📊 SETUP SUMMARY")
    print("=" * 30)
    print(f"Git initialized: {'✅' if git_ok else '❌'}")
    print(f"Required files: {'✅' if files_ok else '❌'}")
    print(f"Environment vars: {'✅' if env_ok else '❌'}")
    print(f".gitignore: {'✅' if gitignore_ok else '❌'}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
    
    # Show next steps
    if not git_ok:
        print(f"\n🔧 Initialize git first:")
        print("   git init")
        print("   git branch -M main")
    
    if files_ok and env_ok:
        git_setup_commands()
        
        print(f"\n🎯 NEXT STEPS:")
        print("1. ✅ Run the git commands above")
        print("2. ✅ Set up GitHub Secrets (see commands above)")
        print("3. ✅ Test workflow: Go to Actions → Run workflow")
        print("4. ✅ Monitor execution in Actions tab")
        
        print(f"\n💡 Your automation will run automatically at:")
        print("   • 9:00 AM UTC (daily)")
        print("   • 2:00 PM UTC (daily)")
        print("   • 6:00 PM UTC (daily)")
        
        print(f"\n📚 Read GITHUB_ACTIONS_SETUP.md for detailed guide!")
    else:
        print(f"\n⚠️ Fix the issues above before proceeding to GitHub setup")

if __name__ == "__main__":
    main()