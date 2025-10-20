#!/usr/bin/env python3
"""
Quick test to verify all imports and basic functionality
"""

def test_imports():
    """Test all required imports"""
    try:
        print("🧪 Testing imports...")
        
        # Core imports
        import os
        import sys
        import requests
        print("✅ Core modules: os, sys, requests")
        
        # RSS and web scraping
        import feedparser
        from bs4 import BeautifulSoup
        print("✅ Web scraping: feedparser, BeautifulSoup")
        
        # Image processing
        from PIL import Image, ImageDraw, ImageFont
        print("✅ Image processing: PIL")
        
        # AI and automation modules
        try:
            import google.generativeai as genai
            print("✅ Gemini AI: google-generativeai")
        except ImportError:
            print("⚠️ Gemini AI: google-generativeai not available")
        
        # Our custom modules
        from enhanced_news_fetcher import EnhancedNewsFetcher
        from news_image_generator import NewsImageGenerator
        print("✅ Custom modules: enhanced_news_fetcher, news_image_generator")
        
        # Test environment variables
        print("\n🔑 Testing environment variables...")
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        print(f"TELEGRAM_BOT_TOKEN: {'✅ Found' if bot_token else '❌ Missing'}")
        print(f"TELEGRAM_CHAT_ID: {'✅ Found' if chat_id else '❌ Missing'}")
        print(f"HUGGINGFACE_TOKEN: {'✅ Found' if hf_token else '❌ Missing'}")
        print(f"GEMINI_API_KEY: {'✅ Found' if gemini_key else '❌ Missing'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Load environment if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    success = test_imports()
    print(f"\n{'✅ All tests passed!' if success else '❌ Tests failed!'}")
    exit(0 if success else 1)