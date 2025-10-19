#!/usr/bin/env python3
"""
GitHub Actions LinkedIn Automation Runner
Optimized version for running in GitHub Actions environment
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any

def setup_github_environment():
    """Setup environment for GitHub Actions"""
    print("🔧 Setting up GitHub Actions environment...")
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("✅ Running in GitHub Actions")
        
        # Set up logging for GitHub Actions
        os.environ['GITHUB_ACTIONS_LOGGING'] = 'true'
        
        # Verify required secrets are available
        required_secrets = [
            'LINKEDIN_ACCESS_TOKEN',
            'LINKEDIN_CLIENT_ID', 
            'LINKEDIN_CLIENT_SECRET'
        ]
        
        missing_secrets = []
        for secret in required_secrets:
            if not os.getenv(secret):
                missing_secrets.append(secret)
        
        if missing_secrets:
            print(f"❌ Missing required secrets: {', '.join(missing_secrets)}")
            return False
        
        print("✅ All required secrets are available")
        return True
    else:
        print("ℹ️ Running locally")
        return True

def run_linkedin_automation():
    """Run the LinkedIn automation in GitHub Actions mode"""
    try:
        print(f"🚀 Starting LinkedIn Automation at {datetime.now().isoformat()}")
        
        # Import and run the main automation
        from main import LinkedInBot
        
        # Create bot instance
        bot = LinkedInBot()
        
        # Run automation with automatic posting enabled
        print("🤖 Running automation with automatic posting...")
        success = bot.run_once(auto_post=True)
        
        if success:
            print("✅ LinkedIn automation completed successfully!")
            
            # Log success for GitHub Actions
            if os.getenv('GITHUB_ACTIONS') == 'true':
                print("::notice::LinkedIn post published successfully")
            
            return True
        else:
            print("❌ LinkedIn automation failed")
            
            # Log failure for GitHub Actions  
            if os.getenv('GITHUB_ACTIONS') == 'true':
                print("::error::LinkedIn automation failed to complete")
            
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Automation error: {str(e)}")
        
        # Log detailed error for GitHub Actions
        if os.getenv('GITHUB_ACTIONS') == 'true':
            print(f"::error::Automation failed with error: {str(e)}")
        
        return False

def save_execution_log(success: bool, details: Dict[str, Any] = None):
    """Save execution log for tracking"""
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'success': success,
        'environment': 'github_actions' if os.getenv('GITHUB_ACTIONS') == 'true' else 'local',
        'details': details or {}
    }
    
    # Save to file for artifact upload
    log_file = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📝 Execution log saved to {log_file}")
        
        # Output for GitHub Actions
        if os.getenv('GITHUB_ACTIONS') == 'true':
            print(f"::set-output name=log_file::{log_file}")
        
    except Exception as e:
        print(f"⚠️ Could not save log: {str(e)}")

def main():
    """Main execution function"""
    print("🤖 LinkedIn Automation - GitHub Actions Runner")
    print("=" * 50)
    
    # Setup environment
    if not setup_github_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Run automation
    start_time = datetime.now()
    success = run_linkedin_automation()
    end_time = datetime.now()
    
    # Calculate execution time
    execution_time = (end_time - start_time).total_seconds()
    
    # Prepare execution details
    details = {
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'execution_time_seconds': execution_time,
        'python_version': sys.version
    }
    
    # Save execution log
    save_execution_log(success, details)
    
    # Summary
    print(f"\n📊 EXECUTION SUMMARY")
    print("=" * 30)
    print(f"Status: {'✅ Success' if success else '❌ Failed'}")
    print(f"Duration: {execution_time:.2f} seconds")
    print(f"Time: {start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')}")
    
    if os.getenv('GITHUB_ACTIONS') == 'true':
        # Set GitHub Actions outputs
        print(f"::set-output name=success::{str(success).lower()}")
        print(f"::set-output name=execution_time::{execution_time}")
        
        if success:
            print("::notice::LinkedIn automation completed successfully in GitHub Actions")
        else:
            print("::warning::LinkedIn automation failed in GitHub Actions")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()