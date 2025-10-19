# LinkedIn Automation Bot Configuration

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LinkedIn API Configuration
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/callback')
    LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
    
    # Hugging Face Configuration
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  # Optional but recommended
    
    # News Configuration
    NEWS_TOPICS = [
        'technology',
        'artificial intelligence',
        'business',
        'startups',
        'programming',
        'linkedin'
    ]
    
    # Content Generation Settings
    MAX_CAPTION_LENGTH = 1300  # LinkedIn character limit
    IMAGE_SIZE = (1200, 630)   # LinkedIn recommended image size
    
    # Posting Schedule (24-hour format)
    POSTING_TIMES = ['10:00', '17:00']  # 10 AM and 5 PM
    
    # File Paths
    IMAGES_DIR = 'generated_images'
    LOGS_DIR = 'logs'
    
    # AI Model Settings
    CAPTION_MODEL = 'facebook/bart-large-cnn'
    IMAGE_MODEL = 'runwayml/stable-diffusion-v1-5'
    
    @staticmethod
    def validate_config():
        """Validate that required configuration is present"""
        required_vars = [
            'LINKEDIN_CLIENT_ID',
            'LINKEDIN_CLIENT_SECRET', 
            'LINKEDIN_ACCESS_TOKEN'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(Config, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True