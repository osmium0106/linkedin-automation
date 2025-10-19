#!/usr/bin/env python3
"""
Quick script to show content summary without loading AI models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_content_manager import LinkedInContentManager

def main():
    print("\n📊 CONTENT SUMMARY")
    print("=" * 50)
    
    try:
        manager = LinkedInContentManager()
        summary = manager.get_posting_summary()
        
        print(f"📄 Total posts ready: {summary['total_posts']}")
        
        if summary['posts_by_topic']:
            print(f"\n📁 Posts by topic:")
            for topic, count in summary['posts_by_topic'].items():
                print(f"   • {topic}: {count} posts")
        
        if summary['recent_posts']:
            print(f"\n🕒 Recent posts:")
            for post in summary['recent_posts'][:5]:  # Show last 5
                print(f"   • {post['created']} - {post['topic']}")
                print(f"     📄 {post['file']}")
        
        if summary['total_posts'] > 0:
            print(f"\n💡 TIP: Check the 'ready_to_post' folder for your content!")
            print(f"🔗 Each post has a posting guide with quick share URLs")
        else:
            print(f"\n🤔 No content ready yet. Run 'python main.py generate' to create some!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error getting content summary: {str(e)}")
        return False

if __name__ == "__main__":
    main()