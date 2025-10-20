"""
Enhanced News Fetcher with duplicate detection and Gemini prompt generation
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import random
import json
import os
import hashlib
from typing import List, Dict
from datetime import datetime, timedelta
import urllib.parse

class EnhancedNewsFetcher:
    def __init__(self):
        self.base_url = "https://news.google.com/rss"
        self.topics = ['technology', 'artificial intelligence', 'AI', 'robotics', 'programming', 'business', 'startups']
        self.used_articles_file = "used_articles.json"
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
    def load_used_articles(self) -> set:
        """Load previously used article IDs"""
        try:
            if os.path.exists(self.used_articles_file):
                with open(self.used_articles_file, 'r') as f:
                    data = json.load(f)
                    # Clean old articles (older than 7 days)
                    cutoff_date = datetime.now() - timedelta(days=7)
                    fresh_articles = {
                        article_id: timestamp for article_id, timestamp in data.items()
                        if datetime.fromisoformat(timestamp) > cutoff_date
                    }
                    return set(fresh_articles.keys())
            return set()
        except Exception as e:
            print(f"⚠️ Error loading used articles: {e}")
            return set()
    
    def save_used_article(self, article_id: str):
        """Save article ID as used"""
        try:
            used_articles = {}
            if os.path.exists(self.used_articles_file):
                with open(self.used_articles_file, 'r') as f:
                    used_articles = json.load(f)
            
            used_articles[article_id] = datetime.now().isoformat()
            
            with open(self.used_articles_file, 'w') as f:
                json.dump(used_articles, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving used article: {e}")
    
    def generate_article_id(self, article: Dict) -> str:
        """Generate unique ID for article based on title and content"""
        content = f"{article['title']}{article['description']}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_google_news_rss(self, topic: str, num_articles: int = 10) -> List[Dict]:
        """
        Fetch fresh news articles from Google News RSS for a specific topic
        
        Args:
            topic: News topic to search for
            num_articles: Number of articles to fetch (increased for more variety)
            
        Returns:
            List of article dictionaries with title, link, description, and published date
        """
        try:
            encoded_topic = urllib.parse.quote_plus(topic)
            # Add time-based query for fresher results
            rss_url = f"{self.base_url}/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
            
            print(f"📰 Fetching fresh news for topic: {topic}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            articles = []
            used_articles = self.load_used_articles()
            
            for entry in feed.entries[:num_articles]:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'description': entry.summary if hasattr(entry, 'summary') else '',
                    'published': entry.published if hasattr(entry, 'published') else str(datetime.now()),
                    'topic': topic,
                    'source': entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
                }
                
                # Generate unique ID and check if not used
                article_id = self.generate_article_id(article)
                article['id'] = article_id
                
                if article_id not in used_articles:
                    articles.append(article)
                else:
                    print(f"⏭️ Skipping duplicate: {article['title'][:50]}...")
            
            print(f"✅ Found {len(articles)} fresh articles for {topic}")
            return articles
            
        except Exception as e:
            print(f"❌ Error fetching news for {topic}: {str(e)}")
            return []
    
    def generate_gemini_prompt(self, article: Dict) -> str:
        """
        Use Gemini AI to generate creative image prompts based on news content
        
        Args:
            article: News article dictionary
            
        Returns:
            AI-generated image prompt
        """
        if not self.gemini_api_key:
            print("⚠️ No Gemini API key found. Add GEMINI_API_KEY to .env")
            return self.generate_fallback_prompt(article)
        
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')  # Use available model
            
            # Create enhanced prompt for Gemini with maximum detail and context
            gemini_input = f"""
You are a world-class AI image prompt engineer specializing in creating ultra-detailed, photorealistic prompts for professional business content. Based on this news article, create an extremely detailed, visually stunning image prompt for AI image generation.

ARTICLE DETAILS:
Title: {article['title']}
Description: {article['description']}
Topic Category: {article['topic']}

DEEP ANALYSIS REQUIRED:
- Extract the core technological/business concept from the article
- Identify specific visual elements that represent the innovation
- Consider the professional LinkedIn business audience
- Think about compelling visual metaphors and storytelling

ULTRA-DETAILED PROMPT REQUIREMENTS:
1. **Scene Composition**: Describe exact camera angle, perspective, framing (wide-shot, close-up, etc.)
2. **Visual Elements**: Specify exact objects, technology, interfaces, people (if relevant)
3. **Lighting & Atmosphere**: Professional lighting setup, color temperature, mood, shadows
4. **Color Palette**: Specific colors that enhance the business/tech theme
5. **Technical Details**: Materials, textures, surfaces, reflections, depth of field
6. **Professional Style**: Corporate photography, architectural photography, product photography style
7. **Quality Specifications**: Ultra-high resolution, photorealistic, commercial grade
8. **Emotional Impact**: Professional, inspiring, innovative, trustworthy feeling

TECHNICAL SPECIFICATIONS:
- Use photography terminology (bokeh, aperture, ISO, etc.)
- Include specific artistic styles (minimalist, futuristic, corporate, etc.)
- Mention exact materials (glass, steel, carbon fiber, etc.)
- Specify lighting types (ambient, dramatic, soft-box, natural, etc.)
- Add composition rules (rule of thirds, leading lines, etc.)

OUTPUT FORMAT:
Create a comprehensive 200-250 word prompt that reads like a professional photography brief. Be extremely specific and detailed. Make it unique to this exact news article content.

Generate the ultra-detailed image prompt now:
"""
            
            print("🤖 Generating creative prompt with Gemini AI...")
            response = model.generate_content(gemini_input)
            
            if response and response.text:
                prompt = response.text.strip()
                print(f"✨ Gemini generated prompt: {prompt[:80]}...")
                return prompt
            else:
                print("⚠️ Gemini returned empty response, using fallback")
                return self.generate_fallback_prompt(article)
                
        except Exception as e:
            print(f"⚠️ Error with Gemini API: {e}")
            print("🔄 Using fallback prompt generation")
            return self.generate_fallback_prompt(article)
    
    def generate_fallback_prompt(self, article: Dict) -> str:
        """Generate enhanced fallback prompt when Gemini is not available"""
        topic = article['topic'].lower()
        title_words = article['title'].lower().split()
        description_words = article['description'].lower().split() if article['description'] else []
        
        # Enhanced topic-based prompts with MAXIMUM detail
        topic_prompts = {
            'ai': "Ultra-modern AI research laboratory, cinematic wide-angle shot, pristine white and chrome surfaces reflecting ambient blue LED lighting, multiple holographic neural network displays floating in mid-air with intricate data pathways glowing in electric blue, sophisticated robotic arms visible in soft-focus background, professional scientists in crisp white lab coats analyzing data on transparent OLED displays, depth of field with sharp foreground focus on floating AI visualization, ambient lighting with subtle rim lighting, photorealistic commercial photography style, shot with 85mm lens at f/2.8, ultra-high resolution 8K detail, corporate innovation aesthetic",
            
            'artificial intelligence': "Dramatic low-angle shot of futuristic AI command center, floor-to-ceiling curved glass displays showing complex machine learning algorithms in real-time, professional data scientist silhouetted against bright analytical dashboards, ambient blue and white lighting creating professional atmosphere, sleek black and silver workstations with multiple curved monitors, holographic brain visualization center-frame with flowing data streams, depth of field focusing on AI interface, commercial architectural photography style, shot with 24-70mm lens, perfect corporate lighting, ultra-detailed 8K resolution, innovation and trust theme",
            
            'robotics': "High-end industrial photography of state-of-the-art robotics facility, precision robotic arms in synchronized motion assembling high-tech components, dramatic industrial lighting with warm amber accents against cool metallic surfaces, ultra-clean white and steel environment with sophisticated automation systems visible throughout, shallow depth of field focusing on robotic precision work, professional commercial photography style shot with macro lens, dramatic shadows and highlights, photorealistic detail showing mechanical precision, corporate manufacturing excellence theme, 8K ultra-high resolution",
            
            'technology': "Cutting-edge technology innovation center interior, dramatic architectural photography with soaring glass ceilings and natural lighting, multiple curved ultra-wide displays showing real-time data analytics, modern professionals collaborating around sleek touch interfaces, ambient blue accent lighting throughout space, minimalist white and glass furniture with chrome accents, depth of field with leading lines drawing eye to central collaboration area, shot with 16-35mm wide-angle lens, professional corporate photography style, ultra-high resolution detail, innovation and collaboration theme",
            
            'business': "Premium corporate boardroom with floor-to-ceiling windows overlooking metropolitan skyline at golden hour, executive team reviewing ascending financial growth charts on massive 4K displays, luxury mahogany conference table with integrated technology, dramatic natural lighting mixed with warm LED accents, professional business attire, depth of field focusing on success metrics, shot with 50mm lens at f/1.8, commercial corporate photography style, ultra-high resolution detail, success and achievement theme, photorealistic quality",
            
            'startups': "Dynamic startup innovation workspace, creative professionals brainstorming around digital whiteboards filled with colorful mind maps and growth charts, modern open-concept office with natural wood accents and living walls, abundant natural lighting through large windows, collaborative energy with laptops and tablets scattered creatively, depth of field focusing on innovation sketches, shot with 35mm lens, documentary-style corporate photography, vibrant yet professional color palette, ultra-detailed 8K resolution, entrepreneurial energy and creativity theme",
            
            'programming': "Ultra-modern software development environment, multiple curved 4K monitors displaying elegant syntax-highlighted code in dark theme, mechanical keyboard with RGB backlighting, sleek minimalist desk setup with premium peripherals, ambient LED strip lighting creating professional coding atmosphere, depth of field focusing on central monitor with code, shot with 85mm lens at f/2.0, tech photography style with dramatic lighting, photorealistic detail of development environment, professional productivity theme, 8K ultra-high resolution"
        }
        
        # Get base detailed prompt
        base_prompt = topic_prompts.get(topic, f"Professional modern {topic} business environment, sleek corporate design, clean minimalist aesthetic, professional lighting, high-end business photography style")
        
        # Add dynamic elements based on title and description keywords
        enhancement_keywords = {
            'breakthrough': ", revolutionary innovation theme, cutting-edge technology elements",
            'innovation': ", innovative design elements, creative technology visualization",
            'new': ", fresh modern approach, contemporary design elements",
            'security': ", digital security visualization, protection and trust elements, secure corporate environment",
            'privacy': ", privacy protection theme, secure data visualization",
            'cyber': ", cybersecurity elements, digital shield concepts, network protection theme",
            'data': ", big data visualization, analytical dashboards, statistical charts and graphs",
            'analytics': ", data analytics theme, business intelligence displays, performance metrics",
            'insights': ", insight visualization, business intelligence theme, strategic analysis elements",
            'growth': ", growth trajectory visualization, ascending business charts, success metrics",
            'market': ", market analysis theme, financial charts, business strategy elements",
            'investment': ", investment and finance theme, portfolio displays, financial growth visualization",
            'startup': ", entrepreneurial energy, innovation workspace, creative collaboration environment",
            'funding': ", venture capital theme, investment visualization, business growth elements"
        }
        
        # Check title and description for enhancement keywords
        all_words = title_words + description_words
        for keyword, enhancement in enhancement_keywords.items():
            if any(keyword in word for word in all_words):
                base_prompt += enhancement
                break
        
        # Add final professional touches with maximum quality specifications
        final_prompt = f"{base_prompt}, professional LinkedIn corporate photography, ultra-high resolution 8K detail, photorealistic commercial quality, perfect lighting and composition, trending on professional photography portfolios, award-winning corporate photography style, shot with professional DSLR camera, perfect exposure and color grading, commercial advertising quality"
        
        return final_prompt
    
    def get_fresh_trending_news(self, num_articles_per_topic: int = 5) -> List[Dict]:
        """
        Get fresh trending news from all configured topics, avoiding duplicates
        
        Args:
            num_articles_per_topic: Number of articles to fetch per topic
            
        Returns:
            List of fresh, unique articles from all topics
        """
        all_articles = []
        
        for topic in self.topics:
            articles = self.get_google_news_rss(topic, num_articles_per_topic)
            all_articles.extend(articles)
        
        # Shuffle for variety
        random.shuffle(all_articles)
        
        print(f"📊 Total fresh articles available: {len(all_articles)}")
        return all_articles
    
    def select_fresh_article(self) -> Dict:
        """
        Select a fresh, unused article and mark it as used
        
        Returns:
            Fresh article dictionary
        """
        articles = self.get_fresh_trending_news()
        
        if not articles:
            print("⚠️ No fresh articles found, trying older articles...")
            # If no fresh articles, clear the used articles and try again
            if os.path.exists(self.used_articles_file):
                os.remove(self.used_articles_file)
            articles = self.get_fresh_trending_news()
        
        if articles:
            selected_article = random.choice(articles)
            
            # Mark as used
            self.save_used_article(selected_article['id'])
            
            print(f"📰 Selected fresh article: {selected_article['title'][:60]}...")
            return selected_article
        else:
            print("❌ No articles available")
            return None

# Test the enhanced functionality
if __name__ == "__main__":
    fetcher = EnhancedNewsFetcher()
    
    # Test fresh article selection
    article = fetcher.select_fresh_article()
    if article:
        print(f"\n✅ Fresh Article Selected:")
        print(f"Title: {article['title']}")
        print(f"Topic: {article['topic']}")
        print(f"ID: {article['id']}")
        
        # Test Gemini prompt generation
        prompt = fetcher.generate_gemini_prompt(article)
        print(f"\n🎨 Generated Prompt:")
        print(prompt)