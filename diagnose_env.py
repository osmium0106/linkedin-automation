#!/usr/bin/env python3
"""
GitHub Actions Diagnostic Script
Helps debug environment issues in GitHub Actions
"""

import os
import sys

def diagnose_environment():
    """Diagnose the GitHub Actions environment"""
    print("🔍 GitHub Actions Environment Diagnostic")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check environment variables
    print("\n🔑 Environment Variables:")
    env_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID', 
        'HUGGINGFACE_TOKEN',
        'GEMINI_API_KEY'
    ]
    
    missing_vars = []
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Found (length: {len(value)})")
        else:
            print(f"❌ {var}: Missing")
            missing_vars.append(var)
    
    # Check required imports
    print("\n📦 Import Tests:")
    import_tests = [
        ('requests', 'requests'),
        ('feedparser', 'feedparser'),
        ('PIL', 'PIL'),
        ('beautifulsoup4', 'bs4'),
        ('google-generativeai', 'google.generativeai'),
        ('python-dotenv', 'dotenv')
    ]
    
    failed_imports = []
    for package, module in import_tests:
        try:
            __import__(module)
            print(f"✅ {package}: Available")
        except ImportError as e:
            print(f"❌ {package}: Missing - {e}")
            failed_imports.append(package)
    
    # Test custom modules
    print("\n🔧 Custom Modules:")
    try:
        from enhanced_news_fetcher import EnhancedNewsFetcher
        print("✅ enhanced_news_fetcher: Available")
    except Exception as e:
        print(f"❌ enhanced_news_fetcher: Failed - {e}")
        failed_imports.append('enhanced_news_fetcher')
    
    try:
        from news_image_generator import NewsImageGenerator
        print("✅ news_image_generator: Available")
    except Exception as e:
        print(f"❌ news_image_generator: Failed - {e}")
        failed_imports.append('news_image_generator')
    
    # Summary
    print("\n📊 Summary:")
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
    if failed_imports:
        print(f"❌ Failed imports: {', '.join(failed_imports)}")
    
    if not missing_vars and not failed_imports:
        print("✅ All checks passed! Environment is ready.")
        return True
    else:
        print("❌ Environment has issues that need to be fixed.")
        return False

if __name__ == "__main__":
    success = diagnose_environment()
    exit(0 if success else 1)