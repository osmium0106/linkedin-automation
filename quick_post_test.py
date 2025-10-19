#!/usr/bin/env python3
"""
Quick automatic posting test using pre-generated content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auto_linkedin_poster import AutoLinkedInPoster

def main():
    print("\n🚀 AUTOMATIC LINKEDIN POSTING TEST")
    print("=" * 50)
    
    # Use pre-made test content
    test_content = """🚀 Exciting developments in tech! Here's what's trending today:

💡 Key insights:
• Innovation continues to reshape our digital landscape
• New technologies are creating unprecedented opportunities
• The future of automation looks incredibly promising

What trends are you most excited about?

#Technology #Innovation #LinkedInAutomation #TechNews #DigitalTransformation

🤖 Posted automatically by LinkedIn Automation Bot"""
    
    print(f"📝 Test content ready ({len(test_content)} characters)")
    print(f"📋 Content preview: {test_content[:100]}...")
    
    try:
        poster = AutoLinkedInPoster()
        
        print(f"\n🔄 Attempting automatic posting...")
        success = poster.auto_post(test_content)
        
        if success:
            print(f"\n✅ SUCCESS! Post was created automatically!")
            print(f"🎉 Your LinkedIn automation is working!")
        else:
            print(f"\n⚠️ Automatic posting failed, but content was prepared for manual posting")
            print(f"📁 Check the 'ready_to_post' folder for your content")
            
            # Ask if user wants to try again with browser automation
            retry = input(f"\n🤔 Try browser automation? (y/n): ").lower().strip()
            if retry == 'y':
                print(f"\n🌐 Opening browser for manual posting...")
                browser_success = poster.post_with_browser_automation(test_content)
                if browser_success:
                    print(f"✅ Browser automation successful!")
                else:
                    print(f"❌ Browser automation failed")
        
        return success
        
    except Exception as e:
        print(f"❌ Error in automatic posting test: {str(e)}")
        return False

if __name__ == "__main__":
    main()