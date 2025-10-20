"""
News Fetcher Module
Fetches trending news from Google News RSS feeds
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import random
from typing import List, Dict
from datetime import datetime
import urllib.parse

class NewsFetcher:
    def __init__(self):
        self.base_url = "https://news.google.com/rss"
        self.topics = ['technology', 'artificial intelligence', 'AI', 'robotics', 'programming', 'business', 'startups']
        
    def get_google_news_rss(self, topic: str, num_articles: int = 5) -> List[Dict]:
        """
        Fetch news articles from Google News RSS for a specific topic
        
        Args:
            topic: News topic to search for
            num_articles: Number of articles to fetch
            
        Returns:
            List of article dictionaries with title, link, description, and published date
        """
        try:
            import urllib.parse
            encoded_topic = urllib.parse.quote_plus(topic)
            # Construct RSS URL for the topic
            rss_url = f"{self.base_url}/search?q={encoded_topic}&hl=en-US&gl=US&ceid=US:en"
            
            print(f"📰 Fetching news for topic: {topic}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            articles = []
            for entry in feed.entries[:num_articles]:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'description': entry.summary if hasattr(entry, 'summary') else '',
                    'published': entry.published if hasattr(entry, 'published') else str(datetime.now()),
                    'topic': topic,
                    'source': entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
                }
                articles.append(article)
                
            print(f"✅ Successfully fetched {len(articles)} articles for {topic}")
            return articles
            
        except Exception as e:
            print(f"❌ Error fetching news for topic {topic}: {str(e)}")
            return []
    
    def get_article_content(self, url: str) -> str:
        """
        Scrape full article content from URL (basic implementation)
        
        Args:
            url: Article URL
            
        Returns:
            Article content as string
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 characters
            
        except Exception as e:
            print(f"⚠️ Could not fetch full content for {url}: {str(e)}")
            return ""
    
    def get_trending_news(self, num_articles_per_topic: int = 3) -> List[Dict]:
        """
        Get trending news from all configured topics
        
        Args:
            num_articles_per_topic: Number of articles to fetch per topic
            
        Returns:
            List of all articles from all topics
        """
        all_articles = []
        
        for topic in self.topics:
            articles = self.get_google_news_rss(topic, num_articles_per_topic)
            all_articles.extend(articles)
            
        print(f"📊 Total articles fetched: {len(all_articles)}")
        return all_articles
    
    def select_random_article(self, articles: List[Dict] = None) -> Dict:
        """
        Select a random article from the provided list or fetch new ones
        
        Args:
            articles: List of articles to choose from. If None, fetches new articles.
            
        Returns:
            Single article dictionary
        """
        if not articles:
            articles = self.get_trending_news()
        
        if not articles:
            raise Exception("No articles available")
        
        selected_article = random.choice(articles)
        
        # Try to get full content
        full_content = self.get_article_content(selected_article['link'])
        if full_content:
            selected_article['full_content'] = full_content
        
        print(f"📰 Selected article: {selected_article['title']}")
        return selected_article
    
    def filter_articles_by_keywords(self, articles: List[Dict], keywords: List[str]) -> List[Dict]:
        """
        Filter articles that contain specific keywords
        
        Args:
            articles: List of articles
            keywords: Keywords to filter by
            
        Returns:
            Filtered list of articles
        """
        filtered_articles = []
        
        for article in articles:
            title_lower = article['title'].lower()
            description_lower = article['description'].lower()
            
            for keyword in keywords:
                if keyword.lower() in title_lower or keyword.lower() in description_lower:
                    filtered_articles.append(article)
                    break
        
        return filtered_articles

# Example usage and testing
if __name__ == "__main__":
    # Initialize news fetcher
    news_fetcher = NewsFetcher()
    
    # Test fetching news
    try:
        # Get trending news
        articles = news_fetcher.get_trending_news(num_articles_per_topic=2)
        print(f"\nFetched {len(articles)} total articles")
        
        # Display first few articles
        for i, article in enumerate(articles[:5]):
            print(f"\n{i+1}. {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   Topic: {article['topic']}")
            print(f"   Description: {article['description'][:100]}...")
        
        # Select a random article
        if articles:
            random_article = news_fetcher.select_random_article(articles)
            print(f"\nSelected random article: {random_article['title']}")
            
    except Exception as e:
        print(f"❌ Error in news fetcher test: {str(e)}")