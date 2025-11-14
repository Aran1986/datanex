# Location: datanex/core/pattern_finder.py

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
from utils.logger import log
import itertools

class PatternFinder:
    """ماژول 6: یافتن الگوها و روابط در داده"""
    
    async def find_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """یافتن همه انواع الگوها"""
        patterns = {
            'correlations': await self._find_correlations(df),
            'trends': await self._find_trends(df),
            'sequences': await self._find_sequences(df),
            'anomalies': await self._find_anomalies(df),
            'associations': await self._find_associations(df),
            'clusters': await self._find_clusters(df)
        }
        
        log.info("Pattern detection completed")
        return patterns
    
    async def _find_correlations(self, df: pd.DataFrame, threshold: float = 0.7) -> List[Dict]:
        """یافتن همبستگی بین ستون‌ها"""
        correlations = []
        
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return correlations
        
        # محاسبه ماتریس همبستگی
        corr_matrix = numeric_df.corr()
        
        # پیدا کردن جفت‌های با همبستگی بالا
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                
                if abs(corr_value) >= threshold:
                    col1 = corr_matrix.columns[i]
                    col2 = corr_matrix.columns[j]
                    
                    correlations.append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': float(corr_value),
                        'type': 'positive' if corr_value > 0 else 'negative',
                        'strength': 'strong' if abs(corr_value) > 0.9 else 'moderate'
                    })
        
        return correlations
    
    async def _find_trends(self, df: pd.DataFrame) -> List[Dict]:
        """یافتن روندهای زمانی"""
        trends = []
        
        # پیدا کردن ستون‌های زمانی
        date_columns = df.select_dtypes(include=['datetime64']).columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        if len(date_columns) == 0 or len(numeric_columns) == 0:
            return trends
        
        for date_col in date_columns:
            df_sorted = df.sort_values(by=date_col)
            
            for num_col in numeric_columns:
                try:
                    # محاسبه شیب روند
                    x = np.arange(len(df_sorted))
                    y = df_sorted[num_col].fillna(method='ffill').fillna(0).values
                    
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                    
                    if abs(r_value) > 0.5:  # همبستگی قابل توجه
                        trends.append({
                            'column': num_col,
                            'date_column': date_col,
                            'trend': 'increasing' if slope > 0 else 'decreasing',
                            'slope': float(slope),
                            'r_squared': float(r_value ** 2),
                            'significance': 'significant' if p_value < 0.05 else 'not_significant'
                        })
                
                except Exception as e:
                    log.debug(f"Could not calculate trend for {num_col}: {e}")
        
        return trends
    
    async def _find_sequences(self, df: pd.DataFrame) -> List[Dict]:
        """یافتن توالی‌های تکراری"""
        sequences = []
        
        # جستجو در ستون‌های categorical
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_columns:
            series = df[col].dropna()
            
            if len(series) < 3:
                continue
            
            # پیدا کردن توالی‌های رایج
            sequence_counts = {}
            window_size = 3
            
            for i in range(len(series) - window_size + 1):
                sequence = tuple(series.iloc[i:i+window_size])
                sequence_counts[sequence] = sequence_counts.get(sequence, 0) + 1
            
            # فیلتر توالی‌های تکراری
            frequent_sequences = [
                {'sequence': list(seq), 'count': count, 'column': col}
                for seq, count in sequence_counts.items()
                if count > 1
            ]
            
            sequences.extend(sorted(frequent_sequences, key=lambda x: x['count'], reverse=True)[:5])
        
        return sequences
    
    async def _find_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """یافتن ناهنجاری‌ها"""
        anomalies = []
        
        numeric_df = df.select_dtypes(include=[np.number])
        
        for column in numeric_df.columns:
            series = df[column].dropna()
            
            if len(series) < 4:
                continue
            
            # روش Z-score
            z_scores = np.abs(stats.zscore(series))
            anomaly_indices = np.where(z_scores > 3)[0]
            
            if len(anomaly_indices) > 0:
                anomalies.append({
                    'column': column,
                    'method': 'z_score',
                    'count': len(anomaly_indices),
                    'anomaly_values': series.iloc[anomaly_indices].tolist()[:10],
                    'mean': float(series.mean()),
                    'std': float(series.std())
                })
        
        return anomalies
    
    async def _find_associations(self, df: pd.DataFrame, min_support: float = 0.1) -> List[Dict]:
        """یافتن قوانین انجمنی (Association Rules)"""
        associations = []
        
        # برای ستون‌های categorical
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        
        if len(categorical_columns) < 2:
            return associations
        
        # محاسبه فراوانی ترکیبات
        for col1, col2 in itertools.combinations(categorical_columns[:5], 2):  # محدود به 5 ستون
            crosstab = pd.crosstab(df[col1], df[col2], normalize='all')
            
            # پیدا کردن ترکیبات رایج
            for idx in crosstab.index:
                for col in crosstab.columns:
                    support = crosstab.loc[idx, col]
                    
                    if support >= min_support:
                        associations.append({
                            'item1': f"{col1}={idx}",
                            'item2': f"{col2}={col}",
                            'support': float(support),
                            'type': 'co_occurrence'
                        })
        
        return sorted(associations, key=lambda x: x['support'], reverse=True)[:20]
    
    async def _find_clusters(self, df: pd.DataFrame, n_components: int = 2) -> Dict[str, Any]:
        """یافتن خوشه‌های طبیعی در داده"""
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        if len(numeric_df) < 10 or len(numeric_df.columns) < 2:
            return {'clusters': [], 'note': 'Insufficient data for clustering'}
        
        try:
            # استانداردسازی
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(numeric_df)
            
            # PCA برای کاهش بعد
            pca = PCA(n_components=min(n_components, len(numeric_df.columns)))
            components = pca.fit_transform(scaled_data)
            
            return {
                'n_components': n_components,
                'explained_variance': pca.explained_variance_ratio_.tolist(),
                'total_variance_explained': float(sum(pca.explained_variance_ratio_)),
                'principal_components': components[:100].tolist()  # فقط 100 اولی
            }
        
        except Exception as e:
            log.error(f"Error in clustering: {e}")
            return {'clusters': [], 'error': str(e)}
    
    async def find_dependencies(self, df: pd.DataFrame) -> List[Dict]:
        """یافتن وابستگی‌های functional"""
        dependencies = []
        
        columns = df.columns.tolist()
        
        # بررسی وابستگی‌های احتمالی
        for col1 in columns:
            for col2 in columns:
                if col1 == col2:
                    continue
                
                # بررسی آیا col1 -> col2 (col1 تعیین‌کننده col2 است)
                grouped = df.groupby(col1)[col2].nunique()
                
                if (grouped == 1).all():
                    dependencies.append({
                        'determinant': col1,
                        'dependent': col2,
                        'type': 'functional_dependency',
                        'confidence': 1.0
                    })
        
        return dependencies
    
    async def analyze_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """تحلیل توزیع داده‌ها"""
        distributions = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            series = df[column].dropna()
            
            if len(series) < 4:
                continue
            
            # آزمون نرمال بودن
            _, p_value = stats.normaltest(series)
            
            distributions[column] = {
                'mean': float(series.mean()),
                'median': float(series.median()),
                'std': float(series.std()),
                'skewness': float(stats.skew(series)),
                'kurtosis': float(stats.kurtosis(series)),
                'is_normal': p_value > 0.05,
                'quartiles': {
                    'Q1': float(series.quantile(0.25)),
                    'Q2': float(series.quantile(0.50)),
                    'Q3': float(series.quantile(0.75))
                }
            }
        
        return distributions

pattern_finder = PatternFinder()