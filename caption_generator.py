"""
Caption Generator Module
Generates LinkedIn-style captions using Hugging Face transformers
"""

import os
import re
from typing import Dict, List
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from loguru import logger
from config import Config

class CaptionGenerator:
    def __init__(self):
        self.config = Config()
        self.model_name = Config.CAPTION_MODEL
        self.max_length = Config.MAX_CAPTION_LENGTH
        self.summarizer = None
        self.tokenizer = None
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model for caption generation"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Use Hugging Face token if available
            use_auth_token = Config.HUGGINGFACE_TOKEN if Config.HUGGINGFACE_TOKEN else None
            
            # Initialize summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                use_auth_token=use_auth_token
            )
            
            # Load tokenizer and model separately for more control
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_auth_token=use_auth_token
            )
            
            logger.success(f"Successfully loaded model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            # Fallback to a simpler model or basic text processing
            self.summarizer = None
    
    def clean_text(self, text: str) -> str:
        """Clean and prepare text for processing"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\\s+', ' ', text)
        
        # Remove special characters that might interfere
        text = re.sub(r'[^\\w\\s.,!?;:()-]', '', text)
        
        # Limit length to avoid token limits
        words = text.split()
        if len(words) > 500:
            text = ' '.join(words[:500])
        
        return text.strip()
    
    def generate_summary(self, article_content: str, max_length: int = 200) -> str:
        """Generate a summary from article content"""
        if not self.summarizer or not article_content:
            return self._fallback_summary(article_content, max_length)
        
        try:
            # Clean the input text
            cleaned_content = self.clean_text(article_content)
            
            if len(cleaned_content) < 50:
                return cleaned_content
            
            # Generate summary
            summary_result = self.summarizer(
                cleaned_content,
                max_length=max_length,
                min_length=50,
                do_sample=False
            )
            
            summary = summary_result[0]['summary_text']
            logger.info(f"Generated summary: {summary[:100]}...")
            
            return summary
            
        except Exception as e:
            logger.warning(f"AI summarization failed, using fallback: {str(e)}")
            return self._fallback_summary(article_content, max_length)
    
    def _fallback_summary(self, content: str, max_length: int) -> str:
        """Fallback method for creating summaries without AI"""
        if not content:
            return "Interesting developments in the tech world today."
        
        # Take first few sentences
        sentences = content.split('.')
        summary = ""
        
        for sentence in sentences:
            if len(summary + sentence) < max_length - 10:
                summary += sentence.strip() + ". "
            else:
                break
        
        return summary.strip()
    
    def create_linkedin_post(self, article: Dict) -> str:
        """
        Create a LinkedIn-style post from a news article
        
        Args:
            article: Dictionary containing article information
            
        Returns:
            LinkedIn post caption as string
        """
        try:
            title = article.get('title', '')
            description = article.get('description', '')
            full_content = article.get('full_content', '')
            topic = article.get('topic', 'news')
            source = article.get('source', 'News')
            
            # Use full content if available, otherwise use description
            content_to_summarize = full_content if full_content else f"{title}. {description}"
            
            # Generate summary
            summary = self.generate_summary(content_to_summarize, max_length=150)
            
            # Create LinkedIn-style post
            post_caption = self._format_linkedin_post(
                title=title,
                summary=summary,
                topic=topic,
                source=source,
                article_url=article.get('link', '')
            )
            
            logger.info(f"Generated LinkedIn post ({len(post_caption)} characters)")
            return post_caption
            
        except Exception as e:
            logger.error(f"Error creating LinkedIn post: {str(e)}")
            return self._create_fallback_post(article)
    
    def _format_linkedin_post(self, title: str, summary: str, topic: str, source: str, article_url: str) -> str:
        """Format the post in LinkedIn style"""
        
        # LinkedIn post templates
        templates = [
            # Template 1: Professional insight
            f"""🚀 {title}

{summary}

💡 Key takeaways:
• This highlights the rapid evolution in {topic}
• Shows the importance of staying updated with industry trends
• Demonstrates how innovation continues to reshape our digital landscape

What are your thoughts on this development?

#LinkedInNews #{topic.replace(' ', '')} #Innovation #Technology

📖 Read more: {article_url}
📰 Source: {source}""",

            # Template 2: Question-focused
            f"""💭 Thought-provoking news from the {topic} world:

{title}

{summary}

🤔 This raises an interesting question: How will this impact professionals in our industry?

I'd love to hear your perspectives in the comments below.

#{topic.replace(' ', '')} #ProfessionalDevelopment #Innovation #Discussion

🔗 Full story: {article_url}""",

            # Template 3: Industry analysis
            f"""📈 Industry Update: {topic.title()}

{title}

{summary}

🎯 Why this matters:
→ Shapes future industry standards
→ Influences market dynamics  
→ Creates new opportunities for growth

What trends are you seeing in your field?

#IndustryNews #{topic.replace(' ', '')} #BusinessInsights #Future

📚 Source: {source}
🔗 {article_url}"""
        ]
        
        # Select a random template and format it
        import random
        selected_template = random.choice(templates)
        
        # Ensure the post doesn't exceed LinkedIn's character limit
        if len(selected_template) > self.max_length:
            # Truncate the summary to fit
            excess_chars = len(selected_template) - self.max_length + 50  # 50 char buffer
            if excess_chars > 0 and len(summary) > excess_chars:
                summary = summary[:-excess_chars] + "..."
                selected_template = selected_template.replace(summary + "...", summary)
        
        return selected_template
    
    def _create_fallback_post(self, article: Dict) -> str:
        """Create a basic post when AI processing fails"""
        title = article.get('title', 'Interesting News Update')
        topic = article.get('topic', 'technology')
        source = article.get('source', 'News')
        article_url = article.get('link', '')
        
        fallback_post = f"""📰 {title}

An important update in the {topic} space that's worth your attention.

Stay informed about the latest developments shaping our industry.

What's your take on this?

#{topic.replace(' ', '')} #News #StayInformed #ProfessionalUpdate

🔗 Read more: {article_url}
📰 Via: {source}"""

        return fallback_post
    
    def add_hashtags(self, text: str, topic: str) -> str:
        """Add relevant hashtags based on the topic"""
        hashtag_map = {
            'technology': ['#Technology', '#Innovation', '#DigitalTransformation', '#TechNews'],
            'artificial intelligence': ['#AI', '#MachineLearning', '#ArtificialIntelligence', '#Innovation', '#FutureTech'],
            'business': ['#Business', '#Entrepreneurship', '#Leadership', '#Strategy', '#GrowthMindset'],
            'startups': ['#Startups', '#Entrepreneurship', '#Innovation', '#Venture', '#BusinessDevelopment'],
            'programming': ['#Programming', '#Development', '#SoftwareEngineering', '#Coding', '#TechSkills'],
            'linkedin': ['#LinkedIn', '#ProfessionalNetworking', '#CareerDevelopment', '#SocialSelling']
        }
        
        relevant_hashtags = hashtag_map.get(topic.lower(), ['#News', '#Professional', '#Industry'])
        
        # Add 3-4 relevant hashtags
        selected_hashtags = relevant_hashtags[:4]
        hashtag_string = ' '.join(selected_hashtags)
        
        return f"{text}\\n\\n{hashtag_string}"

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logger.add("logs/caption_generator.log", rotation="1 day", retention="7 days")
    
    # Sample article for testing
    sample_article = {
        'title': 'New AI Breakthrough Revolutionizes Natural Language Processing',
        'description': 'Scientists have developed a new AI model that can understand context better than ever before, potentially changing how we interact with technology.',
        'full_content': 'A team of researchers has announced a significant breakthrough in natural language processing. The new AI model demonstrates unprecedented ability to understand context, nuance, and implied meaning in human communication. This development could revolutionize chatbots, virtual assistants, and automated content generation systems.',
        'topic': 'artificial intelligence',
        'source': 'Tech Research Journal',
        'link': 'https://example.com/ai-breakthrough'
    }
    
    # Test caption generation
    try:
        caption_generator = CaptionGenerator()
        
        print("Testing LinkedIn Caption Generation...")
        print("=" * 50)
        
        linkedin_post = caption_generator.create_linkedin_post(sample_article)
        
        print("Generated LinkedIn Post:")
        print(linkedin_post)
        print(f"\\nCharacter count: {len(linkedin_post)}")
        print(f"Within LinkedIn limit: {len(linkedin_post) <= Config.MAX_CAPTION_LENGTH}")
        
    except Exception as e:
        logger.error(f"Error in caption generator test: {str(e)}")
        print(f"Error: {str(e)}")