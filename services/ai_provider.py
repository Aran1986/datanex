# Location: datanex/services/ai_provider.py

from typing import List, Dict, Any, Optional
import openai
import anthropic
from utils.config import get_settings
from utils.logger import log

settings = get_settings()

class AIProvider:
    """سرویس AI برای labeling و categorization"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """راه‌اندازی کلاینت‌های AI"""
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.openai_client = openai
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.ANTHROPIC_API_KEY
            )
    
    async def categorize_text(self, text: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """دسته‌بندی متن با AI"""
        if not self.openai_client:
            return {'error': 'OpenAI not configured'}
        
        try:
            prompt = f"Categorize the following text"
            if categories:
                prompt += f" into one of these categories: {', '.join(categories)}"
            prompt += f"\n\nText: {text}\n\nCategory:"
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data categorization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            category = response.choices[0].message.content.strip()
            
            return {
                'text': text[:100],
                'category': category,
                'confidence': 0.8  # OpenAI doesn't provide confidence
            }
            
        except Exception as e:
            log.error(f"Error categorizing text: {e}")
            return {'error': str(e)}
    
    async def label_data(self, data: str, context: Optional[str] = None) -> Dict[str, Any]:
        """لیبل‌گذاری داده با AI"""
        if not self.anthropic_client:
            return {'error': 'Anthropic not configured'}
        
        try:
            prompt = f"Generate descriptive labels for the following data"
            if context:
                prompt += f" in the context of {context}"
            prompt += f":\n\n{data}\n\nProvide 3-5 relevant labels as a comma-separated list."
            
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            labels_text = message.content[0].text
            labels = [label.strip() for label in labels_text.split(',')]
            
            return {
                'data': data[:100],
                'labels': labels
            }
            
        except Exception as e:
            log.error(f"Error labeling data: {e}")
            return {'error': str(e)}
    
    async def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """استخراج entities از متن"""
        if not self.openai_client:
            return []
        
        try:
            prompt = f"Extract named entities (person, organization, location, date, etc.) from this text:\n\n{text}\n\nProvide the result as JSON array with 'entity' and 'type' fields."
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an entity extraction expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.2
            )
            
            # Parse response (simplified)
            entities_text = response.choices[0].message.content
            # در production باید JSON پارس شود
            
            return []
            
        except Exception as e:
            log.error(f"Error extracting entities: {e}")
            return []
    
    async def summarize_dataset(self, data_sample: str) -> str:
        """خلاصه‌سازی dataset"""
        if not self.anthropic_client:
            return "AI summarization not configured"
        
        try:
            prompt = f"Provide a brief summary of this dataset sample:\n\n{data_sample}"
            
            message = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            log.error(f"Error summarizing dataset: {e}")
            return f"Error: {str(e)}"

ai_provider = AIProvider()