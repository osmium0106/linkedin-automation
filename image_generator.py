"""
Image Generator Module
Generates AI images using Stable Diffusion from Hugging Face
"""

import os
import hashlib
from typing import Dict, Optional
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import torch
from diffusers import StableDiffusionPipeline
from loguru import logger
from config import Config

class ImageGenerator:
    def __init__(self):
        self.config = Config()
        self.model_id = Config.IMAGE_MODEL
        self.image_size = Config.IMAGE_SIZE
        self.images_dir = Config.IMAGES_DIR
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Create images directory
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Initialize the model
        self._initialize_pipeline()
    
    def _initialize_pipeline(self):
        """Initialize the Stable Diffusion pipeline"""
        try:
            logger.info(f"Loading Stable Diffusion model: {self.model_id}")
            logger.info(f"Using device: {self.device}")
            
            # Use Hugging Face token if available
            use_auth_token = Config.HUGGINGFACE_TOKEN if Config.HUGGINGFACE_TOKEN else None
            
            # Load the pipeline
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                use_auth_token=use_auth_token
            )
            
            # Move to appropriate device
            self.pipeline = self.pipeline.to(self.device)
            
            # Enable memory efficient attention if using CUDA
            if self.device == "cuda":
                self.pipeline.enable_attention_slicing()
                
            logger.success("Successfully loaded Stable Diffusion pipeline")
            
        except Exception as e:
            logger.error(f"Error loading Stable Diffusion pipeline: {str(e)}")
            logger.warning("AI image generation will be disabled. Using fallback text-based images.")
            self.pipeline = None
    
    def create_prompt_from_article(self, article: Dict) -> str:
        """
        Create an AI image prompt from the news article
        
        Args:
            article: Dictionary containing article information
            
        Returns:
            Image generation prompt as string
        """
        title = article.get('title', '')
        topic = article.get('topic', 'technology')
        description = article.get('description', '')
        
        # Topic-specific prompt templates
        prompt_templates = {
            'technology': [
                f"Professional technology illustration of {title}, modern digital art, clean corporate style, blue and white color scheme, high quality",
                f"Futuristic tech visualization representing {topic}, sleek modern design, professional business aesthetic",
                f"Abstract digital representation of {title}, minimalist corporate design, technology theme"
            ],
            'artificial intelligence': [
                f"AI and machine learning concept art, neural networks, data visualization, professional business style, {title}",
                f"Futuristic AI technology illustration, clean modern design, representing artificial intelligence advancements",
                f"Digital brain and neural network visualization, professional tech aesthetic, AI concept"
            ],
            'business': [
                f"Professional business illustration representing {title}, corporate aesthetic, clean modern design",
                f"Business growth and strategy visualization, professional corporate style, modern office environment",
                f"Corporate business concept art, clean professional design, success and innovation theme"
            ],
            'startups': [
                f"Startup innovation illustration, modern entrepreneurship theme, clean professional design, {title}",
                f"Business launch and growth visualization, professional startup aesthetic, innovation concept",
                f"Entrepreneurship and startup success illustration, modern clean corporate style"
            ],
            'programming': [
                f"Software development illustration, coding and programming theme, clean technical design, {title}",
                f"Developer workspace visualization, modern programming environment, professional tech aesthetic",
                f"Code and software development concept art, clean technical illustration style"
            ]
        }
        
        # Get prompts for the topic or use default
        topic_prompts = prompt_templates.get(topic, prompt_templates['technology'])
        
        # Select the first prompt and enhance it
        base_prompt = topic_prompts[0]
        
        # Add quality and style enhancers
        enhanced_prompt = f"{base_prompt}, highly detailed, professional photography lighting, 8k resolution, trending on artstation"
        
        # Add negative prompt elements to avoid
        negative_elements = "blurry, low quality, distorted, ugly, bad anatomy, text, watermark, signature"
        
        logger.info(f"Generated image prompt: {enhanced_prompt[:100]}...")
        
        return enhanced_prompt, negative_elements
    
    def generate_image(self, article: Dict, save_image: bool = True) -> Optional[str]:
        """
        Generate an AI image based on the article content
        
        Args:
            article: Dictionary containing article information
            save_image: Whether to save the generated image
            
        Returns:
            Path to the generated image file or None if generation failed
        """
        if not self.pipeline:
            logger.warning("Stable Diffusion pipeline not available, creating fallback image")
            return self._create_fallback_image(article, save_image)
        
        try:
            # Create prompt
            prompt, negative_prompt = self.create_prompt_from_article(article)
            
            logger.info("Generating AI image...")
            
            # Generate image
            with torch.autocast(self.device):
                result = self.pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    width=self.image_size[0],
                    height=self.image_size[1],
                    num_inference_steps=20,  # Fewer steps for faster generation
                    guidance_scale=7.5,
                    num_images_per_prompt=1
                )
            
            image = result.images[0]
            
            if save_image:
                # Generate filename based on article title
                filename = self._generate_filename(article.get('title', 'generated_image'))
                filepath = os.path.join(self.images_dir, filename)
                
                # Save image
                image.save(filepath, quality=95, optimize=True)
                
                logger.success(f"AI image saved: {filepath}")
                return filepath
            
            return image
            
        except Exception as e:
            logger.error(f"Error generating AI image: {str(e)}")
            return self._create_fallback_image(article, save_image)
    
    def _create_fallback_image(self, article: Dict, save_image: bool = True) -> Optional[str]:
        """
        Create a simple text-based image when AI generation fails
        
        Args:
            article: Dictionary containing article information
            save_image: Whether to save the image
            
        Returns:
            Path to the created image or Image object
        """
        try:
            # Create a simple colored background image with text
            width, height = self.image_size
            
            # Choose color based on topic
            topic = article.get('topic', 'technology')
            color_schemes = {
                'technology': ('#0077B5', '#FFFFFF'),  # LinkedIn blue
                'artificial intelligence': ('#6B46C1', '#FFFFFF'),  # Purple
                'business': ('#059669', '#FFFFFF'),  # Green
                'startups': ('#DC2626', '#FFFFFF'),  # Red
                'programming': ('#1F2937', '#FFFFFF'),  # Dark gray
            }
            
            bg_color, text_color = color_schemes.get(topic, color_schemes['technology'])
            
            # Create image
            image = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(image)
            
            # Prepare text
            title = article.get('title', 'LinkedIn News Update')
            if len(title) > 60:
                title = title[:57] + "..."
            
            topic_text = f"#{topic.replace(' ', '').title()}"
            
            # Try to load a font (fallback to default if not available)
            try:
                title_font = ImageFont.truetype("arial.ttf", 48)
                topic_font = ImageFont.truetype("arial.ttf", 32)
            except:
                title_font = ImageFont.load_default()
                topic_font = ImageFont.load_default()
            
            # Calculate text positioning
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            
            topic_bbox = draw.textbbox((0, 0), topic_text, font=topic_font)
            topic_width = topic_bbox[2] - topic_bbox[0]
            topic_height = topic_bbox[3] - topic_bbox[1]
            
            # Draw title (wrapped if necessary)
            y_offset = height // 3
            if title_width > width - 100:
                # Wrap text
                words = title.split()
                lines = []
                current_line = ""
                
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    test_bbox = draw.textbbox((0, 0), test_line, font=title_font)
                    test_width = test_bbox[2] - test_bbox[0]
                    
                    if test_width <= width - 100:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                
                if current_line:
                    lines.append(current_line)
                
                # Draw wrapped lines
                for i, line in enumerate(lines):
                    line_bbox = draw.textbbox((0, 0), line, font=title_font)
                    line_width = line_bbox[2] - line_bbox[0]
                    x = (width - line_width) // 2
                    y = y_offset + (i * (title_height + 10))
                    draw.text((x, y), line, fill=text_color, font=title_font)
            else:
                # Single line
                x = (width - title_width) // 2
                draw.text((x, y_offset), title, fill=text_color, font=title_font)
            
            # Draw topic hashtag
            x = (width - topic_width) // 2
            y = height - 100
            draw.text((x, y), topic_text, fill=text_color, font=topic_font)
            
            # Add a simple border
            draw.rectangle([0, 0, width-1, height-1], outline=text_color, width=3)
            
            if save_image:
                # Generate filename
                filename = self._generate_filename(article.get('title', 'fallback_image'))
                filepath = os.path.join(self.images_dir, filename)
                
                # Save image
                image.save(filepath, quality=95, optimize=True)
                
                logger.info(f"Fallback image saved: {filepath}")
                return filepath
            
            return image
            
        except Exception as e:
            logger.error(f"Error creating fallback image: {str(e)}")
            return None
    
    def _generate_filename(self, title: str) -> str:
        """Generate a unique filename based on the title"""
        # Clean the title for filename
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
        
        # Add timestamp and hash for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        
        filename = f"{clean_title}_{timestamp}_{title_hash}.jpg"
        return filename
    
    def resize_image_for_linkedin(self, image_path: str) -> str:
        """
        Resize an image to LinkedIn's recommended dimensions
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Path to the resized image
        """
        try:
            with Image.open(image_path) as img:
                # Resize to LinkedIn recommended size
                resized_img = img.resize(self.image_size, Image.Resampling.LANCZOS)
                
                # Save resized image
                base_name = os.path.splitext(image_path)[0]
                resized_path = f"{base_name}_linkedin.jpg"
                resized_img.save(resized_path, quality=95, optimize=True)
                
                logger.info(f"Image resized for LinkedIn: {resized_path}")
                return resized_path
                
        except Exception as e:
            logger.error(f"Error resizing image: {str(e)}")
            return image_path  # Return original path if resize fails

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logger.add("logs/image_generator.log", rotation="1 day", retention="7 days")
    
    # Sample article for testing
    sample_article = {
        'title': 'Revolutionary AI Model Transforms Business Operations',
        'description': 'A new artificial intelligence system is changing how companies operate worldwide.',
        'topic': 'artificial intelligence',
        'source': 'Tech Today',
    }
    
    # Test image generation
    try:
        image_generator = ImageGenerator()
        
        print("Testing AI Image Generation...")
        print("=" * 50)
        
        # Generate image
        image_path = image_generator.generate_image(sample_article)
        
        if image_path:
            print(f"✅ Image generated successfully: {image_path}")
            print(f"Image size: {image_generator.image_size}")
            
            # Test resizing
            resized_path = image_generator.resize_image_for_linkedin(image_path)
            print(f"✅ Image resized for LinkedIn: {resized_path}")
        else:
            print("❌ Image generation failed")
            
    except Exception as e:
        logger.error(f"Error in image generator test: {str(e)}")
        print(f"Error: {str(e)}")