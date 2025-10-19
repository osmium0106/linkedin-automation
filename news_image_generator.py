"""
AI Image Generator for News Topics
Generates relevant images for LinkedIn posts based on news content
"""

import requests
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict
import json

class NewsImageGenerator:
    def __init__(self):
        self.image_dir = "generated_images"
        self.ensure_image_directory()
        
        # Predefined image templates for different topics
        self.topic_prompts = {
            'AI': "Professional AI technology concept, modern digital interface, blue and purple gradient, clean corporate style, high-tech visualization",
            'artificial intelligence': "Futuristic AI brain network, neural connections, glowing nodes, professional tech background",
            'robotics': "Modern robot technology, sleek robotic arms, industrial automation, clean white background",
            'technology': "Abstract technology patterns, circuit boards, digital innovation, professional blue theme",
            'business': "Modern business concept, professional corporate style, growth charts, success visualization",
            'startups': "Innovation concept, lightbulb with gears, entrepreneurship, modern gradient background",
            'programming': "Code snippets on screen, programming languages, developer workspace, clean modern style",
            'machine learning': "Data visualization, neural networks, algorithm patterns, professional tech design",
            'data science': "Data analytics visualization, charts and graphs, professional dashboard style",
            'cybersecurity': "Digital security concept, shield with binary code, protection theme, blue accent",
            'blockchain': "Blockchain network visualization, connected blocks, cryptocurrency theme, modern design",
            'cloud computing': "Cloud infrastructure diagram, server networks, professional IT design",
            'mobile': "Smartphone technology, mobile app interface, modern device design",
            'web development': "Website wireframes, responsive design, web interface mockup",
            'software': "Software architecture diagram, application development, code structure visualization"
        }
    
    def ensure_image_directory(self):
        """Ensure the images directory exists"""
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
    
    def generate_prompt_from_news(self, title: str, description: str, topic: str) -> str:
        """
        Generate an AI image prompt based on news content
        
        Args:
            title: News article title
            description: News article description  
            topic: News topic category
            
        Returns:
            Generated prompt for AI image generation
        """
        # Get base prompt for topic
        base_prompt = self.topic_prompts.get(topic.lower(), self.topic_prompts.get('technology'))
        
        # Extract key terms from title
        key_terms = []
        tech_keywords = ['AI', 'robot', 'automation', 'machine learning', 'neural', 'algorithm', 
                        'data', 'cloud', 'blockchain', 'software', 'app', 'digital', 'cyber',
                        'innovation', 'startup', 'tech', 'compute', 'platform', 'API']
        
        title_words = title.lower().split()
        for keyword in tech_keywords:
            if keyword.lower() in title.lower():
                key_terms.append(keyword)
        
        # Create enhanced prompt
        if key_terms:
            enhanced_prompt = f"{base_prompt}, featuring {', '.join(key_terms[:3])}, professional LinkedIn post style"
        else:
            enhanced_prompt = f"{base_prompt}, professional LinkedIn post style"
            
        return enhanced_prompt
    
    def generate_image_huggingface(self, prompt: str, filename: str) -> Optional[str]:
        """
        Generate image using Hugging Face Inference API (free tier)
        
        Args:
            prompt: Text prompt for image generation
            filename: Output filename
            
        Returns:
            Path to generated image or None if failed
        """
        try:
            # Use Hugging Face's free Stable Diffusion model
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            
            # Try to get token from environment
            token = os.getenv('HUGGINGFACE_TOKEN')
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512
                }
            }
            
            print(f"🎨 Generating image with prompt: {prompt[:60]}...")
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                image_path = os.path.join(self.image_dir, filename)
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Image generated: {filename}")
                return image_path
            else:
                print(f"⚠️ Hugging Face API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error generating image: {e}")
            return None
    
    def create_text_based_image(self, title: str, topic: str, filename: str) -> str:
        """
        Create a simple text-based image as fallback
        
        Args:
            title: News title
            topic: News topic
            filename: Output filename
            
        Returns:
            Path to created image
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            # Create image
            width, height = 800, 600
            background_colors = {
                'AI': '#4A90E2',
                'technology': '#2E8B57', 
                'business': '#FF6B35',
                'robotics': '#9B59B6',
                'programming': '#E74C3C'
            }
            
            bg_color = background_colors.get(topic, '#34495E')
            
            img = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a font
            try:
                font_title = ImageFont.truetype("arial.ttf", 36)
                font_topic = ImageFont.truetype("arial.ttf", 24)
            except:
                font_title = ImageFont.load_default()
                font_topic = ImageFont.load_default()
            
            # Wrap title text
            wrapped_title = textwrap.fill(title[:80], width=25)
            
            # Draw topic
            topic_text = f"#{topic.upper()}"
            draw.text((50, 50), topic_text, fill='white', font=font_topic)
            
            # Draw title
            draw.text((50, 150), wrapped_title, fill='white', font=font_title)
            
            # Draw timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d")
            draw.text((50, height-80), f"Generated: {timestamp}", fill='lightgray', font=font_topic)
            
            # Save image
            image_path = os.path.join(self.image_dir, filename)
            img.save(image_path)
            print(f"✅ Text-based image created: {filename}")
            return image_path
            
        except Exception as e:
            print(f"⚠️ Error creating text image: {e}")
            # Return a placeholder path
            return None
    
    def generate_news_image(self, news_data: Dict) -> Optional[str]:
        """
        Generate an image for a news article
        
        Args:
            news_data: Dictionary containing news article data
            
        Returns:
            Path to generated image or None if failed
        """
        title = news_data.get('title', '')
        description = news_data.get('description', '')
        topic = news_data.get('topic', 'technology')
        
        # Create filename based on content
        content_hash = hashlib.md5(f"{title}{topic}".encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_{topic}_{timestamp}_{content_hash}.jpg"
        
        # Try AI generation first
        prompt = self.generate_prompt_from_news(title, description, topic)
        image_path = self.generate_image_huggingface(prompt, filename)
        
        # Fallback to text-based image
        if not image_path:
            print("🔄 Falling back to text-based image...")
            try:
                image_path = self.create_text_based_image(title, topic, filename)
            except:
                # Final fallback - create a simple placeholder
                image_path = self.create_simple_placeholder(filename, topic)
        
        return image_path
    
    def create_simple_placeholder(self, filename: str, topic: str) -> str:
        """Create a very simple placeholder image"""
        try:
            # Create a simple HTML-to-image placeholder
            placeholder_content = f"""
            <div style="width:800px;height:600px;background:linear-gradient(45deg,#667eea,#764ba2);
                        display:flex;align-items:center;justify-content:center;color:white;
                        font-family:Arial;text-align:center;font-size:36px;">
                <div>
                    <h2>📰 LinkedIn News</h2>
                    <p>#{topic.upper()}</p>
                    <p style="font-size:16px;">{datetime.now().strftime("%Y-%m-%d")}</p>
                </div>
            </div>
            """
            
            # Save as HTML file and convert to image would require additional tools
            # For now, return None to use default behavior
            return None
            
        except:
            return None

# Test function
def test_image_generation():
    """Test the image generation functionality"""
    generator = NewsImageGenerator()
    
    test_news = {
        'title': 'OpenAI Announces Revolutionary GPT-5 with Advanced Reasoning',
        'description': 'New AI model shows breakthrough capabilities in complex reasoning tasks',
        'topic': 'AI'
    }
    
    image_path = generator.generate_news_image(test_news)
    if image_path:
        print(f"✅ Test image generated: {image_path}")
    else:
        print("❌ Test image generation failed")

if __name__ == "__main__":
    test_image_generation()