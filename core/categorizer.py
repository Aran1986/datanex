# Location: datanex/core/categorizer.py

import pandas as pd
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from utils.logger import log
import re

class Categorizer:
    """ماژول 2: دسته‌بندی داده‌ها"""
    
    # دسته‌بندی‌های از پیش تعریف شده
    PREDEFINED_CATEGORIES = {
        'financial': ['price', 'cost', 'amount', 'payment', 'salary', 'revenue', 'expense'],
        'personal': ['name', 'email', 'phone', 'address', 'age', 'gender'],
        'temporal': ['date', 'time', 'timestamp', 'year', 'month', 'day'],
        'location': ['country', 'city', 'state', 'zip', 'latitude', 'longitude'],
        'identifier': ['id', 'uuid', 'key', 'code', 'number'],
        'text': ['description', 'comment', 'note', 'message', 'content'],
        'boolean': ['status', 'active', 'enabled', 'flag'],
        'metric': ['count', 'total', 'average', 'percentage', 'ratio']
    }
    
    async def categorize_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """دسته‌بندی ستون‌ها بر اساس نام و محتوا"""
        categories = {}
        
        for column in df.columns:
            category = await self._detect_column_category(column, df[column])
            categories[column] = category
        
        log.info(f"Categorized {len(categories)} columns")
        return categories
    
    async def _detect_column_category(self, column_name: str, series: pd.Series) -> str:
        """تشخیص دسته یک ستون"""
        column_lower = column_name.lower()
        
        # بررسی بر اساس نام ستون
        for category, keywords in self.PREDEFINED_CATEGORIES.items():
            if any(keyword in column_lower for keyword in keywords):
                return category
        
        # بررسی بر اساس نوع داده
        if pd.api.types.is_numeric_dtype(series):
            if series.nunique() < 10:
                return 'categorical_numeric'
            return 'metric'
        
        elif pd.api.types.is_datetime64_any_dtype(series):
            return 'temporal'
        
        elif pd.api.types.is_bool_dtype(series):
            return 'boolean'
        
        elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
            # بررسی الگوهای خاص
            sample = series.dropna().head(100).astype(str)
            
            if sample.str.match(r'^[\w\.-]+@[\w\.-]+\.\w+$').any():
                return 'personal'
            
            if sample.str.match(r'^\d{4}-\d{2}-\d{2}').any():
                return 'temporal'
            
            if sample.str.len().mean() > 100:
                return 'text'
            
            if series.nunique() < len(series) * 0.5:
                return 'categorical_text'
            
            return 'text'
        
        return 'unknown'
    
    async def categorize_data_semantic(self, df: pd.DataFrame, n_categories: int = 5) -> Dict[str, Any]:
        """دسته‌بندی معنایی داده‌ها با ML"""
        if len(df) < 10:
            return {'categories': [], 'method': 'insufficient_data'}
        
        try:
            # ترکیب تمام ستون‌های متنی
            text_columns = df.select_dtypes(include=['object']).columns
            if len(text_columns) == 0:
                return {'categories': [], 'method': 'no_text_data'}
            
            # آماده‌سازی متن برای TF-IDF
            texts = df[text_columns].fillna('').astype(str).agg(' '.join, axis=1)
            
            # TF-IDF Vectorization
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            X = vectorizer.fit_transform(texts)
            
            # K-Means Clustering
            n_clusters = min(n_categories, len(df) // 2)
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            labels = kmeans.fit_predict(X)
            
            # استخراج کلمات کلیدی هر دسته
            categories = []
            feature_names = vectorizer.get_feature_names_out()
            
            for i in range(n_clusters):
                cluster_center = kmeans.cluster_centers_[i]
                top_indices = cluster_center.argsort()[-5:][::-1]
                top_keywords = [feature_names[idx] for idx in top_indices]
                
                categories.append({
                    'id': i,
                    'size': int((labels == i).sum()),
                    'keywords': top_keywords,
                    'representative_rows': df[labels == i].head(3).to_dict('records')
                })
            
            return {
                'categories': categories,
                'method': 'kmeans_tfidf',
                'n_clusters': n_clusters
            }
            
        except Exception as e:
            log.error(f"Error in semantic categorization: {e}")
            return {'categories': [], 'method': 'error', 'error': str(e)}
    
    async def categorize_by_domain(self, df: pd.DataFrame) -> List[str]:
        """تشخیص حوزه/دامنه داده"""
        domains = set()
        
        all_text = ' '.join([str(col) for col in df.columns])
        all_text += ' ' + ' '.join([str(val) for val in df.head(10).values.flatten()])
        all_text = all_text.lower()
        
        domain_keywords = {
            'ecommerce': ['product', 'price', 'order', 'cart', 'customer', 'shipping'],
            'finance': ['transaction', 'balance', 'account', 'payment', 'invoice'],
            'healthcare': ['patient', 'doctor', 'diagnosis', 'treatment', 'medical'],
            'education': ['student', 'course', 'grade', 'teacher', 'exam'],
            'social_media': ['post', 'like', 'comment', 'follower', 'share'],
            'analytics': ['metric', 'event', 'session', 'conversion', 'funnel'],
            'hr': ['employee', 'salary', 'department', 'position', 'performance'],
            'logistics': ['shipment', 'delivery', 'warehouse', 'tracking', 'inventory']
        }
        
        for domain, keywords in domain_keywords.items():
            if sum(keyword in all_text for keyword in keywords) >= 2:
                domains.add(domain)
        
        return list(domains) if domains else ['general']

categorizer = Categorizer()