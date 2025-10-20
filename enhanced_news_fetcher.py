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
            
            # Create enhanced prompt for Gemini with more context
            gemini_input = f"""
You are a professional AI image prompt creator for LinkedIn business content. Based on this news article, create a detailed, visually compelling image prompt for AI image generation.

ARTICLE DETAILS:
Title: {article['title']}
Description: {article['description']}
Topic Category: {article['topic']}

CONTEXT ANALYSIS:
- Analyze the main theme and key concepts from the title and description
- Identify visual metaphors that represent the core message
- Consider the business/professional audience on LinkedIn

PROMPT REQUIREMENTS:
1. Create a highly detailed, specific visual scene (not generic)
2. Include specific visual elements, colors, lighting, and composition
3. Focus on professional, modern, corporate aesthetic suitable for LinkedIn
4. Use visual metaphors that clearly relate to the article content
5. Specify camera angle, depth of field, and artistic style
6. Make it engaging and visually striking
7. Avoid mentioning specific companies, people, or brand names
8. Include technical photography terms for better AI generation
9. Target 150-200 words for maximum detail
10. Make it unique and creative, not template-based

OUTPUT FORMAT:
Provide only the detailed image prompt, nothing else. Make it comprehensive and specific.

Generate the detailed image prompt now:
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
        
        # Enhanced topic-based prompts with more detail
        topic_prompts = {
            'ai': "Professional futuristic AI laboratory scene, multiple holographic neural network displays floating in air, interconnected data nodes with glowing blue pathways, sleek glass surfaces reflecting digital patterns, ambient blue and white lighting, ultra-modern corporate setting, depth of field, cinematic composition, high detail, professional photography style",
            'artificial intelligence': "Advanced AI research facility interior, scientist analyzing complex machine learning algorithms on transparent displays, robotic arms working in background, digital brain visualization with flowing data streams, professional blue and silver color scheme, modern glass architecture, corporate technology aesthetic, 8k detail",
            'robotics': "State-of-the-art robotics manufacturing floor, precision robotic arms assembling high-tech components, clean white and metallic environment, dramatic industrial lighting, sophisticated automation systems, modern factory setting, professional corporate photography, shallow depth of field focusing on robotic precision",
            'technology': "Cutting-edge technology innovation center, multiple curved displays showing data analytics, sleek modern workstations, professionals collaborating on digital interfaces, ambient blue lighting, glass and steel architecture, corporate innovation theme, professional business photography",
            'business': "Modern corporate boardroom with floor-to-ceiling windows overlooking city skyline, professional executives reviewing growth charts on large displays, ascending financial graphs, premium wood and glass furniture, natural lighting, success and achievement theme, corporate luxury aesthetic",
            'startups': "Dynamic startup workspace with creative professionals brainstorming, whiteboards filled with innovative concepts, modern open office design, natural lighting, plants and modern furniture, collaboration and innovation theme, energetic and inspiring atmosphere, professional documentary style",
            'programming': "Modern software development environment, multiple monitors displaying elegant code syntax, clean minimalist workspace, keyboard and mouse setup, ambient desk lighting, professional developer setup, blue and green accent lighting, high-tech productivity theme, corporate tech aesthetic"
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
        
        # Add final professional touches
        final_prompt = f"{base_prompt}, professional LinkedIn corporate style, high resolution, photorealistic, commercial photography quality, trending on business photography, professional corporate aesthetic, clean composition"
        
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