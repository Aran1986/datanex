# Location: datanex/core/validator.py

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from great_expectations.dataset import PandasDataset
from utils.logger import log
import re
from datetime import datetime

class Validator:
    """ماژول 4: تشخیص داده‌های خراب و اعتبارسنجی"""
    
    # الگوهای معتبر
    PATTERNS = {
        'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
        'phone': r'^\+?1?\d{9,15}$',
        'url': r'^https?://[\w\.-]+\.\w+',
        'ipv4': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        'credit_card': r'^\d{13,19}$',
        'postal_code': r'^\d{5}(-\d{4})?$',
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    }
    
    async def validate_data(self, df: pd.DataFrame, rules: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """اعتبارسنجی کامل داده"""
        validation_results = {
            'is_valid': True,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'invalid_rows': [],
            'column_issues': {},
            'summary': {}
        }
        
        # بررسی مقادیر null
        null_check = await self._check_null_values(df)
        validation_results['column_issues']['null_values'] = null_check
        
        # بررسی outliers
        outlier_check = await self._check_outliers(df)
        validation_results['column_issues']['outliers'] = outlier_check
        
        # بررسی انواع داده
        dtype_check = await self._check_data_types(df)
        validation_results['column_issues']['data_types'] = dtype_check
        
        # بررسی محدوده‌ها
        range_check = await self._check_ranges(df)
        validation_results['column_issues']['ranges'] = range_check
        
        # بررسی الگوها
        pattern_check = await self._check_patterns(df)
        validation_results['column_issues']['patterns'] = pattern_check
        
        # بررسی قوانین سفارشی
        if rules:
            custom_check = await self._check_custom_rules(df, rules)
            validation_results['column_issues']['custom_rules'] = custom_check
        
        # شناسایی ردیف‌های خراب
        invalid_rows = await self._identify_invalid_rows(df, validation_results['column_issues'])
        validation_results['invalid_rows'] = invalid_rows
        validation_results['invalid_count'] = len(invalid_rows)
        
        # خلاصه
        validation_results['summary'] = {
            'total_issues': sum(len(v) for v in validation_results['column_issues'].values() if isinstance(v, list)),
            'invalid_ratio': len(invalid_rows) / len(df) if len(df) > 0 else 0,
            'quality_score': await self._calculate_quality_score(validation_results)
        }
        
        validation_results['is_valid'] = validation_results['summary']['quality_score'] > 0.7
        
        log.info(f"Validation completed. Quality score: {validation_results['summary']['quality_score']:.2f}")
        return validation_results
    
    async def _check_null_values(self, df: pd.DataFrame) -> Dict[str, Any]:
        """بررسی مقادیر null"""
        null_info = {}
        
        for column in df.columns:
            null_count = df[column].isnull().sum()
            if null_count > 0:
                null_info[column] = {
                    'count': int(null_count),
                    'percentage': float(null_count / len(df) * 100),
                    'indices': df[df[column].isnull()].index.tolist()[:100]  # فقط 100 اولی
                }
        
        return null_info
    
    async def _check_outliers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """تشخیص outliers در ستون‌های عددی"""
        outlier_info = {}
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            series = df[column].dropna()
            
            if len(series) < 4:
                continue
            
            # روش IQR
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
            
            if len(outliers) > 0:
                outlier_info[column] = {
                    'count': len(outliers),
                    'percentage': float(len(outliers) / len(df) * 100),
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'outlier_values': outliers[column].tolist()[:50]
                }
        
        return outlier_info
    
    async def _check_data_types(self, df: pd.DataFrame) -> Dict[str, Any]:
        """بررسی سازگاری انواع داده"""
        dtype_issues = {}
        
        for column in df.columns:
            series = df[column]
            
            # بررسی ستون‌های object که باید numeric باشند
            if series.dtype == 'object':
                # سعی در تبدیل به numeric
                numeric_converted = pd.to_numeric(series, errors='coerce')
                non_numeric_count = numeric_converted.isnull().sum() - series.isnull().sum()
                
                if non_numeric_count > 0 and non_numeric_count < len(series) * 0.9:
                    # احتمالاً باید numeric باشد اما مقادیر غیرعددی دارد
                    non_numeric_values = series[numeric_converted.isnull() & series.notnull()].unique()[:10]
                    dtype_issues[column] = {
                        'issue': 'mixed_numeric_text',
                        'non_numeric_count': int(non_numeric_count),
                        'sample_values': non_numeric_values.tolist()
                    }
            
            # بررسی مقادیر منفی در جایی که نباید باشد
            if pd.api.types.is_numeric_dtype(series):
                if 'count' in column.lower() or 'quantity' in column.lower() or 'age' in column.lower():
                    negative_count = (series < 0).sum()
                    if negative_count > 0:
                        dtype_issues[column] = {
                            'issue': 'unexpected_negative_values',
                            'negative_count': int(negative_count)
                        }
        
        return dtype_issues
    
    async def _check_ranges(self, df: pd.DataFrame) -> Dict[str, Any]:
        """بررسی محدوده‌های منطقی"""
        range_issues = {}
        
        # قوانین محدوده برای فیلدهای شناخته شده
        range_rules = {
            'age': (0, 120),
            'percentage': (0, 100),
            'rating': (0, 5),
            'score': (0, 100),
            'temperature': (-100, 100),
            'humidity': (0, 100)
        }
        
        for column in df.columns:
            column_lower = column.lower()
            
            for field_name, (min_val, max_val) in range_rules.items():
                if field_name in column_lower:
                    series = df[column].dropna()
                    
                    if pd.api.types.is_numeric_dtype(series):
                        out_of_range = ((series < min_val) | (series > max_val)).sum()
                        
                        if out_of_range > 0:
                            range_issues[column] = {
                                'expected_range': [min_val, max_val],
                                'out_of_range_count': int(out_of_range),
                                'min_found': float(series.min()),
                                'max_found': float(series.max())
                            }
        
        return range_issues
    
    async def _check_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """بررسی الگوهای خاص"""
        pattern_issues = {}
        
        for column in df.columns:
            column_lower = column.lower()
            series = df[column].dropna().astype(str)
            
            if len(series) == 0:
                continue
            
            # تشخیص نوع فیلد و بررسی الگو
            for field_type, pattern in self.PATTERNS.items():
                if field_type in column_lower:
                    invalid = ~series.str.match(pattern, na=False)
                    invalid_count = invalid.sum()
                    
                    if invalid_count > 0:
                        pattern_issues[column] = {
                            'expected_pattern': field_type,
                            'invalid_count': int(invalid_count),
                            'invalid_percentage': float(invalid_count / len(series) * 100),
                            'sample_invalid': series[invalid].head(10).tolist()
                        }
                    break
        
        return pattern_issues
    
    async def _check_custom_rules(self, df: pd.DataFrame, rules: List[Dict]) -> List[Dict]:
        """اعمال قوانین سفارشی"""
        custom_issues = []
        
        for rule in rules:
            try:
                rule_name = rule.get('name', 'unnamed_rule')
                column = rule.get('column')
                condition = rule.get('condition')
                
                if column not in df.columns:
                    continue
                
                # ارزیابی شرط
                if condition == 'not_null':
                    violations = df[df[column].isnull()]
                elif condition == 'unique':
                    violations = df[df[column].duplicated(keep=False)]
                elif 'min' in rule:
                    violations = df[df[column] < rule['min']]
                elif 'max' in rule:
                    violations = df[df[column] > rule['max']]
                else:
                    continue
                
                if len(violations) > 0:
                    custom_issues.append({
                        'rule': rule_name,
                        'column': column,
                        'violation_count': len(violations),
                        'violation_indices': violations.index.tolist()[:100]
                    })
            
            except Exception as e:
                log.error(f"Error checking custom rule: {e}")
        
        return custom_issues
    
    async def _identify_invalid_rows(self, df: pd.DataFrame, column_issues: Dict) -> List[int]:
        """شناسایی ردیف‌های خراب"""
        invalid_indices = set()
        
        # جمع‌آوری همه ایندکس‌های مشکل‌دار
        for issue_type, issues in column_issues.items():
            if isinstance(issues, dict):
                for column, details in issues.items():
                    if isinstance(details, dict) and 'indices' in details:
                        invalid_indices.update(details['indices'])
        
        return sorted(list(invalid_indices))[:1000]  # محدود به 1000 ردیف
    
    async def _calculate_quality_score(self, validation_results: Dict) -> float:
        """محاسبه امتیاز کیفی"""
        total_rows = validation_results['total_rows']
        
        if total_rows == 0:
            return 0.0
        
        # وزن‌های مختلف برای مسائل
        weights = {
            'null_values': 0.3,
            'outliers': 0.2,
            'data_types': 0.2,
            'ranges': 0.15,
            'patterns': 0.15
        }
        
        score = 1.0
        
        for issue_type, weight in weights.items():
            issues = validation_results['column_issues'].get(issue_type, {})
            
            if isinstance(issues, dict):
                issue_count = sum(
                    details.get('count', details.get('invalid_count', 0))
                    for details in issues.values()
                    if isinstance(details, dict)
                )
                
                penalty = (issue_count / total_rows) * weight
                score -= penalty
        
        return max(0.0, min(1.0, score))
    
    async def clean_data(self, df: pd.DataFrame, validation_results: Dict, strategy: str = 'drop') -> pd.DataFrame:
        """پاکسازی داده‌های خراب"""
        cleaned_df = df.copy()
        
        if strategy == 'drop':
            # حذف ردیف‌های خراب
            invalid_indices = validation_results.get('invalid_rows', [])
            cleaned_df = cleaned_df.drop(index=invalid_indices)
            log.info(f"Dropped {len(invalid_indices)} invalid rows")
        
        elif strategy == 'fill':
            # پر کردن مقادیر null
            null_info = validation_results['column_issues'].get('null_values', {})
            
            for column, details in null_info.items():
                if column in cleaned_df.columns:
                    if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                        # با میانگین پر کن
                        cleaned_df[column].fillna(cleaned_df[column].mean(), inplace=True)
                    else:
                        # با مقدار رایج‌ترین پر کن
                        mode_val = cleaned_df[column].mode()
                        if len(mode_val) > 0:
                            cleaned_df[column].fillna(mode_val[0], inplace=True)
            
            log.info(f"Filled null values in {len(null_info)} columns")
        
        elif strategy == 'flag':
            # علامت‌گذاری ردیف‌های خراب
            invalid_indices = validation_results.get('invalid_rows', [])
            cleaned_df['is_valid'] = True
            cleaned_df.loc[invalid_indices, 'is_valid'] = False
            log.info(f"Flagged {len(invalid_indices)} invalid rows")
        
        return cleaned_df

validator = Validator()