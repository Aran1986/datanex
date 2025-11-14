# Location: datanex/core/labeler.py

import pandas as pd
from typing import List, Dict, Any, Optional
from utils.logger import log
from sentence_transformers import SentenceTransformer
import numpy as np

class Labeler:
    """ماژول 3: لیبل‌گذاری و تگ‌گذاری خودکار"""
    
    def __init__(self):
        # مدل برای similarity detection
        self.model = None
    
    def _load_model(self):
        """بارگذاری مدل embedding"""
        if self.model is None:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def auto_label_columns(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """لیبل‌گذاری خودکار ستون‌ها"""
        labels = {}
        
        for column in df.columns:
            column_labels = await self._generate_column_labels(column, df[column])
            labels[column] = column_labels
        
        return labels
    
    async def _generate_column_labels(self, column_name: str, series: pd.Series) -> Dict[str, Any]:
        """تولید لیبل برای یک ستون"""
        labels = {
            'column_name': column_name,
            'data_type': str(series.dtype),
            'tags': [],
            'quality': {}
        }
        
        # تگ‌های کیفیت داده
        null_ratio = series.isnull().sum() / len(series)
        labels['quality']['completeness'] = 1 - null_ratio
        labels['quality']['null_count'] = int(series.isnull().sum())
        
        if null_ratio > 0.5:
            labels['tags'].append('high_missing_data')
        elif null_ratio > 0.1:
            labels['tags'].append('moderate_missing_data')
        else:
            labels['tags'].append('complete_data')
        
        # تگ‌های یکتایی
        uniqueness = series.nunique() / len(series)
        labels['quality']['uniqueness'] = uniqueness
        
        if uniqueness > 0.95:
            labels['tags'].append('unique_identifier')
        elif uniqueness < 0.01:
            labels['tags'].append('constant_value')
        elif uniqueness < 0.1:
            labels['tags'].append('low_cardinality')
        
        # تگ‌های نوع داده
        if pd.api.types.is_numeric_dtype(series):
            labels['tags'].append('numeric')
            
            # بررسی توزیع
            if series.dropna().std() / (series.dropna().mean() + 1e-10) < 0.1:
                labels['tags'].append('low_variance')
            
            # بررسی outlier
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((series < (Q1 - 1.5 * IQR)) | (series > (Q3 + 1.5 * IQR))).sum()
            if outliers > len(series) * 0.05:
                labels['tags'].append('has_outliers')
                labels['quality']['outlier_count'] = int(outliers)
        
        elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
            labels['tags'].append('text')
            
            # بررسی طول متن
            avg_length = series.dropna().astype(str).str.len().mean()
            if avg_length > 100:
                labels['tags'].append('long_text')
            elif avg_length < 10:
                labels['tags'].append('short_text')
        
        elif pd.api.types.is_datetime64_any_dtype(series):
            labels['tags'].append('temporal')
        
        return labels
    
    async def generate_tags(self, df: pd.DataFrame, custom_rules: Optional[List[Dict]] = None) -> List[str]:
        """تولید تگ‌های کلی برای dataset"""
        tags = []
        
        # تگ‌های سایز
        if len(df) < 100:
            tags.append('small_dataset')
        elif len(df) < 10000:
            tags.append('medium_dataset')
        else:
            tags.append('large_dataset')
        
        # تگ‌های کیفیت
        total_null_ratio = df.isnull().sum().sum() / (len(df) * len(df.columns))
        if total_null_ratio < 0.01:
            tags.append('high_quality')
        elif total_null_ratio > 0.3:
            tags.append('low_quality')
        
        # تگ‌های ساختار
        if len(df.columns) < 5:
            tags.append('simple_structure')
        elif len(df.columns) > 50:
            tags.append('complex_structure')
        
        # تگ‌های نوع داده
        numeric_ratio = len(df.select_dtypes(include='number').columns) / len(df.columns)
        if numeric_ratio > 0.7:
            tags.append('mostly_numeric')
        elif numeric_ratio < 0.3:
            tags.append('mostly_text')
        else:
            tags.append('mixed_data')
        
        # اعمال قوانین سفارشی
        if custom_rules:
            for rule in custom_rules:
                if await self._check_custom_rule(df, rule):
                    tags.append(rule.get('tag', 'custom'))
        
        return tags
    
    async def _check_custom_rule(self, df: pd.DataFrame, rule: Dict) -> bool:
        """بررسی یک قانون سفارشی"""
        try:
            condition = rule.get('condition', '')
            # اجرای شرط به صورت ایمن
            # در نسخه واقعی باید از یک DSL امن استفاده شود
            return False
        except:
            return False
    
    async def suggest_labels_ml(self, df: pd.DataFrame, sample_size: int = 1000) -> Dict[str, List[str]]:
        """پیشنهاد لیبل با ML"""
        self._load_model()
        suggestions = {}
        
        try:
            # نمونه‌گیری برای کارایی بهتر
            sample_df = df.head(sample_size) if len(df) > sample_size else df
            
            for column in sample_df.columns:
                if pd.api.types.is_string_dtype(sample_df[column]) or pd.api.types.is_object_dtype(sample_df[column]):
                    texts = sample_df[column].dropna().astype(str).tolist()[:100]
                    
                    if texts:
                        # استخراج کلمات کلیدی با embedding similarity
                        embeddings = self.model.encode(texts)
                        
                        # محاسبه مرکز cluster
                        center = np.mean(embeddings, axis=0)
                        
                        # پیدا کردن نزدیک‌ترین متن‌ها به مرکز
                        similarities = np.dot(embeddings, center)
                        top_indices = similarities.argsort()[-3:][::-1]
                        
                        suggested_labels = [texts[i] for i in top_indices]
                        suggestions[column] = suggested_labels
            
            return suggestions
            
        except Exception as e:
            log.error(f"Error in ML label suggestion: {e}")
            return {}

labeler = Labeler()