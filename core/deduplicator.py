# Location: datanex/core/deduplicator.py

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils.logger import log
import hashlib

class Deduplicator:
    """ماژول 5: تشخیص و حذف داده‌های تکراری"""
    
    def __init__(self):
        self.model = None
    
    def _load_model(self):
        """بارگذاری مدل برای semantic similarity"""
        if self.model is None:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def find_duplicates(self, df: pd.DataFrame, method: str = 'exact') -> Dict[str, Any]:
        """پیدا کردن تکراری‌ها"""
        
        if method == 'exact':
            result = await self._find_exact_duplicates(df)
        elif method == 'fuzzy':
            result = await self._find_fuzzy_duplicates(df)
        elif method == 'semantic':
            result = await self._find_semantic_duplicates(df)
        elif method == 'hybrid':
            result = await self._find_hybrid_duplicates(df)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        log.info(f"Found {result['duplicate_count']} duplicates using {method} method")
        return result
    
    async def _find_exact_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """تشخیص تکراری‌های دقیق"""
        duplicates = df[df.duplicated(keep=False)]
        duplicate_groups = []
        
        if len(duplicates) > 0:
            # گروه‌بندی تکراری‌ها
            for _, group in duplicates.groupby(list(df.columns)):
                if len(group) > 1:
                    duplicate_groups.append({
                        'size': len(group),
                        'indices': group.index.tolist(),
                        'sample': group.iloc[0].to_dict()
                    })
        
        return {
            'method': 'exact',
            'duplicate_count': len(duplicates),
            'duplicate_groups': duplicate_groups,
            'unique_count': len(df) - len(duplicates) + len(duplicate_groups)
        }
    
    async def _find_fuzzy_duplicates(self, df: pd.DataFrame, threshold: float = 0.85) -> Dict[str, Any]:
        """تشخیص تکراری‌های fuzzy با نام‌های متفاوت"""
        duplicate_groups = []
        processed_indices = set()
        
        # ایجاد هش برای هر ردیف (نادیده گرفتن تفاوت‌های جزئی)
        def fuzzy_hash(row):
            # نرمال‌سازی و هش
            normalized = []
            for val in row:
                if pd.isna(val):
                    normalized.append('NULL')
                elif isinstance(val, str):
                    # حذف فاصله‌ها و تبدیل به lowercase
                    normalized.append(val.strip().lower())
                else:
                    normalized.append(str(val))
            return hashlib.md5('|'.join(normalized).encode()).hexdigest()
        
        # محاسبه هش برای هر ردیف
        hashes = df.apply(fuzzy_hash, axis=1)
        
        # پیدا کردن گروه‌های مشابه
        for hash_val, group in df.groupby(hashes):
            if len(group) > 1:
                duplicate_groups.append({
                    'size': len(group),
                    'indices': group.index.tolist(),
                    'sample': group.iloc[0].to_dict(),
                    'variations': group.to_dict('records')[:5]
                })
                processed_indices.update(group.index)
        
        return {
            'method': 'fuzzy',
            'duplicate_count': len(processed_indices),
            'duplicate_groups': duplicate_groups,
            'unique_count': len(df) - len(processed_indices) + len(duplicate_groups)
        }
    
    async def _find_semantic_duplicates(self, df: pd.DataFrame, threshold: float = 0.9) -> Dict[str, Any]:
        """تشخیص تکراری‌های معنایی"""
        self._load_model()
        duplicate_groups = []
        
        try:
            # ترکیب ستون‌های متنی
            text_columns = df.select_dtypes(include=['object']).columns
            if len(text_columns) == 0:
                return {
                    'method': 'semantic',
                    'duplicate_count': 0,
                    'duplicate_groups': [],
                    'unique_count': len(df),
                    'note': 'No text columns for semantic comparison'
                }
            
            # ایجاد متن ترکیبی
            texts = df[text_columns].fillna('').astype(str).agg(' '.join, axis=1).tolist()
            
            # محدود کردن برای عملکرد بهتر
            max_rows = 1000
            if len(texts) > max_rows:
                log.warning(f"Dataset too large for semantic deduplication. Using first {max_rows} rows.")
                texts = texts[:max_rows]
                df_sample = df.head(max_rows)
            else:
                df_sample = df
            
            # ایجاد embeddings
            embeddings = self.model.encode(texts, show_progress_bar=False)
            
            # محاسبه شباهت
            similarity_matrix = cosine_similarity(embeddings)
            
            # پیدا کردن جفت‌های مشابه
            processed = set()
            
            for i in range(len(similarity_matrix)):
                if i in processed:
                    continue
                
                # پیدا کردن ردیف‌های مشابه
                similar_indices = np.where(similarity_matrix[i] >= threshold)[0]
                
                if len(similar_indices) > 1:
                    group_indices = df_sample.iloc[similar_indices].index.tolist()
                    duplicate_groups.append({
                        'size': len(similar_indices),
                        'indices': group_indices,
                        'similarity_scores': similarity_matrix[i][similar_indices].tolist(),
                        'sample': df_sample.iloc[i].to_dict(),
                        'variations': df_sample.iloc[similar_indices].to_dict('records')[:3]
                    })
                    processed.update(similar_indices)
            
            duplicate_count = len(processed)
            
            return {
                'method': 'semantic',
                'duplicate_count': duplicate_count,
                'duplicate_groups': duplicate_groups,
                'unique_count': len(df_sample) - duplicate_count + len(duplicate_groups),
                'threshold': threshold
            }
        
        except Exception as e:
            log.error(f"Error in semantic deduplication: {e}")
            return {
                'method': 'semantic',
                'duplicate_count': 0,
                'duplicate_groups': [],
                'unique_count': len(df),
                'error': str(e)
            }
    
    async def _find_hybrid_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """ترکیب روش‌های مختلف"""
        # اول exact
        exact_result = await self._find_exact_duplicates(df)
        exact_indices = set()
        for group in exact_result['duplicate_groups']:
            exact_indices.update(group['indices'])
        
        # حذف exact duplicates
        df_remaining = df.drop(index=list(exact_indices))
        
        # سپس fuzzy روی باقی‌مانده
        fuzzy_result = await self._find_fuzzy_duplicates(df_remaining)
        fuzzy_indices = set()
        for group in fuzzy_result['duplicate_groups']:
            fuzzy_indices.update(group['indices'])
        
        # ترکیب نتایج
        all_groups = exact_result['duplicate_groups'] + fuzzy_result['duplicate_groups']
        
        return {
            'method': 'hybrid',
            'duplicate_count': len(exact_indices) + len(fuzzy_indices),
            'duplicate_groups': all_groups,
            'unique_count': len(df) - len(exact_indices) - len(fuzzy_indices) + len(all_groups),
            'breakdown': {
                'exact': len(exact_indices),
                'fuzzy': len(fuzzy_indices)
            }
        }
    
    async def remove_duplicates(self, df: pd.DataFrame, duplicate_result: Dict, keep: str = 'first') -> pd.DataFrame:
        """حذف تکراری‌ها"""
        df_clean = df.copy()
        
        indices_to_drop = []
        
        for group in duplicate_result['duplicate_groups']:
            group_indices = group['indices']
            
            if keep == 'first':
                # حذف همه به جز اولی
                indices_to_drop.extend(group_indices[1:])
            elif keep == 'last':
                # حذف همه به جز آخری
                indices_to_drop.extend(group_indices[:-1])
            elif keep == 'none':
                # حذف همه
                indices_to_drop.extend(group_indices)
        
        df_clean = df_clean.drop(index=indices_to_drop)
        
        log.info(f"Removed {len(indices_to_drop)} duplicate rows")
        return df_clean
    
    async def merge_duplicates(self, df: pd.DataFrame, duplicate_result: Dict, strategy: str = 'prefer_complete') -> pd.DataFrame:
        """ادغام تکراری‌ها به جای حذف"""
        df_merged = df.copy()
        
        for group in duplicate_result['duplicate_groups']:
            group_indices = group['indices']
            group_data = df.loc[group_indices]
            
            if strategy == 'prefer_complete':
                # ترجیح ردیفی که کمترین null دارد
                null_counts = group_data.isnull().sum(axis=1)
                best_idx = null_counts.idxmin()
                merged_row = group_data.loc[best_idx]
                
                # پر کردن null‌های merged_row از سایر ردیف‌ها
                for idx in group_indices:
                    if idx != best_idx:
                        for col in df.columns:
                            if pd.isna(merged_row[col]) and not pd.isna(group_data.loc[idx, col]):
                                merged_row[col] = group_data.loc[idx, col]
                
                # حذف بقیه و جایگزینی با merged
                df_merged = df_merged.drop(index=[i for i in group_indices if i != best_idx])
                df_merged.loc[best_idx] = merged_row
            
            elif strategy == 'aggregate':
                # ترکیب مقادیر
                merged_row = {}
                for col in df.columns:
                    col_data = group_data[col].dropna()
                    
                    if len(col_data) == 0:
                        merged_row[col] = None
                    elif pd.api.types.is_numeric_dtype(col_data):
                        merged_row[col] = col_data.mean()
                    else:
                        merged_row[col] = col_data.mode()[0] if len(col_data.mode()) > 0 else col_data.iloc[0]
                
                # نگه داشتن اولین ردیف و حذف بقیه
                first_idx = group_indices[0]
                df_merged = df_merged.drop(index=group_indices[1:])
                df_merged.loc[first_idx] = pd.Series(merged_row)
        
        log.info(f"Merged duplicate groups using {strategy} strategy")
        return df_merged

deduplicator = Deduplicator()