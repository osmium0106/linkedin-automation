"""
AI Image Generator for News Topics with Enhanced News Fetching and Gemini Integration
Generates relevant images for LinkedIn posts based on fresh news content
"""

import requests
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict
import json
import time
from enhanced_news_fetcher import EnhancedNewsFetcher

class NewsImageGenerator:
    def __init__(self):
        self.image_dir = "generated_images"
        self.ensure_image_directory()
        self.news_fetcher = EnhancedNewsFetcher()  # Use enhanced news fetcher
        
        # Keep fallback prompts as backup
        self.topic_prompts = {
            'AI': "Professional AI technology visualization, neural network patterns, glowing blue nodes, futuristic interface design, clean corporate style, high-tech digital art, 4k quality",
            'artificial intelligence': "Advanced AI brain concept, interconnected neural pathways, luminous data flows, sophisticated machine learning visualization, professional tech aesthetic",
            'robotics': "Sleek modern robot technology, precision mechanical arms, advanced automation systems, industrial innovation, clean minimalist design, professional lighting",
            'technology': "Cutting-edge technology concept, digital innovation patterns, circuit board aesthetics, modern tech interface, professional blue and silver theme, corporate style",
            'business': "Modern business growth concept, ascending charts and graphs, professional corporate environment, success visualization, clean design, premium quality",
            'startups': "Innovation and entrepreneurship concept, creative lightbulb with digital elements, modern workspace, growth trajectory, inspiring design, professional quality",
            'programming': "Clean code development environment, multiple programming languages, elegant syntax highlighting, developer workspace, modern IDE interface, professional setup",
            'machine learning': "Data science visualization, algorithmic patterns, statistical models, advanced analytics dashboard, professional data representation, modern design",
            'data science': "Advanced data analytics, interactive charts and visualizations, big data concepts, professional dashboard interface, modern statistical design",
            'cybersecurity': "Digital security shield concept, encrypted data protection, cyber defense visualization, network security, professional blue accent, trust and safety theme",
            'blockchain': "Distributed ledger visualization, interconnected blockchain nodes, cryptocurrency network, decentralized technology, modern fintech design",
            'cloud computing': "Cloud infrastructure visualization, distributed server networks, scalable computing resources, professional IT architecture, modern tech design",
            'mobile': "Modern smartphone innovation, sleek mobile interface design, app development concept, responsive design, professional mobile technology",
            'web development': "Modern web interface design, responsive website layouts, clean user experience, professional web development, modern design principles",
            'software': "Software architecture visualization, application development lifecycle, code structure patterns, professional development environment, modern tech aesthetic"
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
        # Extract key concepts from the news title and description
        combined_text = f"{title} {description}".lower()
        
        # Tech-specific keywords to look for in the news
        tech_concepts = {
            'ai': ['artificial intelligence', 'machine learning', 'neural network', 'deep learning', 'ai model', 'chatgpt', 'openai', 'gpt'],
            'robotics': ['robot', 'automation', 'robotic', 'autonomous', 'drone', 'mechanical', 'android'],
            'blockchain': ['blockchain', 'cryptocurrency', 'bitcoin', 'ethereum', 'crypto', 'web3', 'nft'],
            'cloud': ['cloud computing', 'aws', 'azure', 'google cloud', 'server', 'infrastructure'],
            'mobile': ['smartphone', 'mobile', 'app', 'ios', 'android', 'iphone', 'samsung'],
            'security': ['cybersecurity', 'security', 'hack', 'breach', 'privacy', 'encryption'],
            'data': ['data science', 'analytics', 'big data', 'database', 'visualization'],
            'software': ['software', 'programming', 'code', 'developer', 'framework', 'api'],
            'startup': ['startup', 'funding', 'investment', 'vc', 'entrepreneur', 'innovation'],
            'business': ['business', 'company', 'corporate', 'market', 'industry', 'revenue']
        }
        
        # Identify the main concept from the news
        detected_concepts = []
        for concept, keywords in tech_concepts.items():
            for keyword in keywords:
                if keyword in combined_text:
                    detected_concepts.append(concept)
                    break
        
        # Create a specific prompt based on detected concepts and actual news content
        if 'ai' in detected_concepts:
            base_prompt = "Professional AI and machine learning technology, futuristic neural networks with glowing connections, modern tech interface, blue and purple gradient background, digital innovation theme"
        elif 'robotics' in detected_concepts:
            base_prompt = "Advanced robotics and automation technology, sleek modern robots, industrial automation, clean futuristic design, metallic surfaces with blue accents"
        elif 'blockchain' in detected_concepts:
            base_prompt = "Blockchain network visualization, interconnected digital blocks, cryptocurrency concept, modern financial technology, geometric patterns with blue lighting"
        elif 'cloud' in detected_concepts:
            base_prompt = "Cloud computing infrastructure, server networks in data centers, modern IT technology, professional business environment with blue accents"
        elif 'mobile' in detected_concepts:
            base_prompt = "Modern smartphone and mobile technology, sleek app interfaces, contemporary device design, digital lifestyle theme"
        elif 'security' in detected_concepts:
            base_prompt = "Cybersecurity and digital protection, shield with binary code, secure technology concepts, professional security theme with green accents"
        elif 'data' in detected_concepts:
            base_prompt = "Data analytics and visualization, modern charts and graphs, business intelligence dashboard, professional data science theme"
        elif 'software' in detected_concepts:
            base_prompt = "Software development and programming, clean code interfaces, modern developer workspace, tech innovation theme"
        elif 'startup' in detected_concepts:
            base_prompt = "Innovation and startup growth, ascending arrows, entrepreneurship energy, modern business success visualization"
        elif 'business' in detected_concepts:
            base_prompt = "Professional business and corporate success, modern office environment, growth achievement theme, clean corporate aesthetic"
        else:
            # Default tech prompt based on the actual topic
            base_prompt = f"Modern {topic} technology concept, abstract digital patterns, innovation and progress theme, professional tech background"
        
        # Add LinkedIn-specific styling and high quality parameters
        final_prompt = f"{base_prompt}, professional LinkedIn post style, high quality, clean composition, suitable for social media, corporate aesthetic, digital art, trending on artstation"
        
        return final_prompt
    
    def generate_smart_prompt(self, article: Dict) -> str:
        """
        Generate smart image prompt using Gemini AI or fallback to enhanced prompts
        
        Args:
            article: News article dictionary with title, description, topic
            
        Returns:
            AI-generated or enhanced prompt for image generation
        """
        try:
            # Try Gemini first for creative prompts
            return self.news_fetcher.generate_gemini_prompt(article)
        except Exception as e:
            print(f"⚠️ Error with smart prompt generation: {e}")
            # Fallback to enhanced manual prompts
            return self.generate_prompt_from_news(
                article['title'], 
                article['description'], 
                article['topic']
            )
    
    def generate_image_for_fresh_news(self) -> Optional[Dict]:
        """
        Generate image for a fresh news article with smart prompting
        
        Returns:
            Dictionary with image path, article info, and prompt used
        """
        # Get fresh article
        article = self.news_fetcher.select_fresh_article()
        if not article:
            print("❌ No fresh articles available")
            return None
        
        # Generate smart prompt
        smart_prompt = self.generate_smart_prompt(article)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        article_hash = article['id'][:8]  # Use article ID for uniqueness
        filename = f"news_{article['topic'].replace(' ', '_')}_{timestamp}_{article_hash}.jpg"
        
        print(f"🎨 Generating AI image for fresh news...")
        print(f"📰 Article: {article['title'][:60]}...")
        
        # Generate image
        image_path = self.generate_image_huggingface(smart_prompt, filename)
        
        if image_path:
            # Add logo overlay
            image_with_logo = self.add_logo_overlay(image_path)
            
            # Add title overlay
            if image_with_logo:
                final_path = self.add_title_overlay(image_with_logo, article['title'])
                if final_path:
                    return {
                        'image_path': final_path,
                        'article': article,
                        'prompt': smart_prompt,
                        'filename': filename
                    }
        
        # Fallback to text-based image
        print("🔄 Generating fallback text-based image...")
        fallback_path = self.create_text_based_image(
            article['title'], 
            article['topic'], 
            filename.replace('.jpg', '_text.jpg')
        )
        
        if fallback_path:
            # Add logo and title to fallback image too
            image_with_logo = self.add_logo_overlay(fallback_path)
            final_path = self.add_title_overlay(image_with_logo or fallback_path, article['title'])
            return {
                'image_path': final_path or fallback_path,
                'article': article,
                'prompt': smart_prompt,
                'filename': filename,
                'fallback': True
            }
        
        return None
    
    def generate_image_huggingface(self, prompt: str, filename: str) -> Optional[str]:
        """
        Generate image using Hugging Face Inference API with proper waiting and retry logic
        
        Args:
            prompt: Text prompt for image generation
            filename: Output filename
            
        Returns:
            Path to generated image or None if failed
        """
        import time
        
        try:
            # Use the working FLUX model we discovered
            API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
            
            # Get token from environment
            token = os.getenv('HUGGINGFACE_TOKEN')
            if not token:
                print("⚠️ No Hugging Face token found. Add HUGGINGFACE_TOKEN to .env for AI images")
                return None
                
            headers = {"Authorization": f"Bearer {token}"}
            
            # FLUX.1-schnell specific parameters (optimized for maximum quality)
            payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 12,  # Increased from 8 for maximum quality
                    "guidance_scale": 5.0,     # Higher for more detailed images
                    "width": 1024,
                    "height": 1024
                }
            }
            
            print(f"🎨 Generating high-quality AI image with FLUX.1-schnell...")
            print(f"🔖 Prompt: {prompt[:80]}...")
            print(f"⏳ Using 12 inference steps with extended processing time (60+ seconds for best quality)...")
            
            # FLUX with extended time for maximum quality (1 minute+ timeout)
            max_retries = 3  # Increased retries for better success rate
            retry_delay = 25  # Longer delay between retries for better quality
            
            for attempt in range(max_retries):
                print(f"🔄 Attempt {attempt + 1}/{max_retries}...")
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=90)  # Extended timeout to 90 seconds
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'application/json' in content_type:
                        try:
                            error_data = response.json()
                            error_msg = error_data.get('error', 'Unknown error')
                            
                            if 'loading' in error_msg.lower():
                                estimated_time = error_data.get('estimated_time', retry_delay)
                                print(f"⏳ FLUX model loading... waiting {estimated_time + 10} seconds for better quality")
                                time.sleep(estimated_time + 15)  # Extended wait time for quality
                                continue
                            else:
                                print(f"❌ FLUX API Error: {error_msg}")
                                break
                        except:
                            print("❌ JSON parsing error")
                            break
                    else:
                        # Success! We got image data
                        if len(response.content) > 1000:
                            image_path = os.path.join(self.image_dir, filename)
                            with open(image_path, "wb") as f:
                                f.write(response.content)
                            print(f"✅ Amazing FLUX AI image generated: {filename}")
                            
                            # Add logo overlay if logo exists
                            final_image_path = self.add_logo_overlay(image_path)
                            if final_image_path:
                                print(f"🏷️ Logo added to image!")
                                return final_image_path
                            else:
                                print(f"🚀 High-quality image ready for LinkedIn!")
                                return image_path
                        else:
                            print("⚠️ Received invalid image data")
                            continue
                            
                elif response.status_code == 503:
                    print(f"🔄 FLUX model loading... waiting {retry_delay + 10} seconds for optimal generation")
                    time.sleep(retry_delay + 15)  # Extended wait for better quality
                    continue
                    
                elif response.status_code == 401:
                    print("❌ Authentication failed. Check your HUGGINGFACE_TOKEN")
                    return None
                    
                else:
                    print(f"⚠️ HTTP {response.status_code}: {response.text[:100]}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                
            print("❌ Failed to generate FLUX image after retries")
            return None
                
        except Exception as e:
            print(f"⚠️ Error generating AI image: {e}")
            return None
    
    def add_logo_overlay(self, image_path: str) -> Optional[str]:
        """
        Add ThinkersKlub logo to the top-right corner of generated image
        
        Args:
            image_path: Path to the generated image
            
        Returns:
            Path to image with logo overlay, or None if failed
        """
        try:
            from PIL import Image, ImageDraw
            
            # Logo file paths to try - prioritize user's actual logo
            logo_paths = [
                "thinkersklub_logo_circular.png",  # User's actual logo (PRIORITY)
                "logo.png", 
                "assets/thinkersklub_logo_circular.png",
                "images/thinkersklub_logo_circular.png"
            ]
            
            logo_path = None
            for path in logo_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if not logo_path:
                print("⚠️ Logo file 'thinkersklub_logo_circular.png' not found")
                print("💡 Place your logo in the root directory for automatic overlay")
                return image_path  # Return original image path, not None
            
            # Open the generated image
            main_image = Image.open(image_path)
            
            # Open and resize logo
            logo = Image.open(logo_path)
            
            # Calculate logo size (15% of image width for better visibility)
            logo_size = int(main_image.width * 0.15)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Ensure logo has transparency
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            # Position: top-right corner with 20px margin
            margin = 20
            logo_position = (
                main_image.width - logo_size - margin,
                margin
            )
            
            # Convert main image to RGBA if needed
            if main_image.mode != 'RGBA':
                main_image = main_image.convert('RGBA')
            
            # Create a transparent overlay
            overlay = Image.new('RGBA', main_image.size, (0, 0, 0, 0))
            overlay.paste(logo, logo_position, logo)
            
            # Composite the images
            final_image = Image.alpha_composite(main_image, overlay)
            
            # Convert back to RGB for saving as JPEG
            if final_image.mode == 'RGBA':
                rgb_image = Image.new('RGB', final_image.size, (255, 255, 255))
                rgb_image.paste(final_image, mask=final_image.split()[-1])
                final_image = rgb_image
            
            # Save the final image
            final_image.save(image_path, 'JPEG', quality=95)
            print(f"✅ ThinkersKlub logo added to image!")
            
            return image_path
            
        except Exception as e:
            print(f"⚠️ Error adding logo: {e}")
            print("💡 Make sure 'thinkersklub_logo_circular.png' is in the project directory")
            return None
    
    def add_title_overlay(self, image_path: str, title: str) -> Optional[str]:
        """
        Add news title as text overlay on the bottom of the image
        
        Args:
            image_path: Path to the image
            title: News title to overlay
            
        Returns:
            Path to image with title overlay, or None if failed
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap
            
            # Open the image
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)
            
            # Clean and truncate title
            clean_title = title.replace(" - ", " | ").strip()
            if len(clean_title) > 100:
                clean_title = clean_title[:97] + "..."
            
            # Try to use a better font
            try:
                # Try different font sizes
                font_size = min(32, max(20, img.width // 25))  # Dynamic font size
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("calibri.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Wrap text to fit image width
            max_width = img.width - 40  # Leave 20px margin on each side
            wrapped_lines = []
            
            # Split title into words and wrap
            words = clean_title.split()
            current_line = ""
            
            for word in words:
                test_line = f"{current_line} {word}".strip()
                bbox = draw.textbbox((0, 0), test_line, font=font)
                text_width = bbox[2] - bbox[0]
                
                if text_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        wrapped_lines.append(current_line)
                        current_line = word
                    else:
                        wrapped_lines.append(word)
            
            if current_line:
                wrapped_lines.append(current_line)
            
            # Limit to 2 lines max
            if len(wrapped_lines) > 2:
                wrapped_lines = wrapped_lines[:2]
                wrapped_lines[1] = wrapped_lines[1][:50] + "..." if len(wrapped_lines[1]) > 50 else wrapped_lines[1]
            
            # Calculate text area height
            line_height = 40
            text_area_height = len(wrapped_lines) * line_height + 20  # Add padding
            
            # Create semi-transparent overlay at bottom
            overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            
            # Draw semi-transparent background for text
            text_bg_y = img.height - text_area_height
            overlay_draw.rectangle(
                [0, text_bg_y, img.width, img.height], 
                fill=(0, 0, 0, 180)  # Semi-transparent black
            )
            
            # Composite overlay with main image
            img = Image.alpha_composite(img.convert('RGBA'), overlay)
            draw = ImageDraw.Draw(img)
            
            # Draw text lines
            y_position = img.height - text_area_height + 10
            for line in wrapped_lines:
                # Center text horizontally
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x_position = (img.width - text_width) // 2
                
                # Draw text with white color
                draw.text((x_position, y_position), line, fill=(255, 255, 255, 255), font=font)
                y_position += line_height
            
            # Convert back to RGB and save
            if img.mode == 'RGBA':
                rgb_image = Image.new('RGB', img.size, (255, 255, 255))
                rgb_image.paste(img, mask=img.split()[-1])
                img = rgb_image
            
            img.save(image_path, 'JPEG', quality=95)
            print(f"📰 News title added to image!")
            
            return image_path
            
        except Exception as e:
            print(f"⚠️ Error adding title overlay: {e}")
            return image_path  # Return original path if overlay fails
    
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
            
            # Try to add logo to text-based image too
            final_image_path = self.add_logo_overlay(image_path)
            if final_image_path:
                print(f"🏷️ Logo added to text-based image!")
                return final_image_path
            else:
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