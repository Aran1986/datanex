# Location: datanex/core/scraper.py

import asyncio
from typing import List, Dict, Any, Optional
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Browser, Page
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
import requests
from utils.logger import log
import json
import re
from urllib.parse import urljoin, urlparse

class Scraper:
    """ماژول اسکرپ و ردیابی داده از وب"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def scrape_url(self, url: str, method: str = 'requests') -> Dict[str, Any]:
        """اسکرپ یک URL"""
        
        if method == 'requests':
            return await self._scrape_with_requests(url)
        elif method == 'playwright':
            return await self._scrape_with_playwright(url)
        elif method == 'scrapy':
            return await self._scrape_with_scrapy(url)
        else:
            raise ValueError(f"Unknown scraping method: {method}")
    
    async def _scrape_with_requests(self, url: str) -> Dict[str, Any]:
        """اسکرپ ساده با requests"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # استخراج اطلاعات
            data = {
                'url': url,
                'status_code': response.status_code,
                'title': soup.title.string if soup.title else None,
                'text': soup.get_text(strip=True, separator=' '),
                'links': [urljoin(url, a.get('href', '')) for a in soup.find_all('a', href=True)],
                'images': [urljoin(url, img.get('src', '')) for img in soup.find_all('img', src=True)],
                'meta': self._extract_meta_tags(soup),
                'structured_data': self._extract_structured_data(soup)
            }
            
            log.info(f"Successfully scraped {url} with requests")
            return data
            
        except Exception as e:
            log.error(f"Error scraping {url}: {e}")
            return {'url': url, 'error': str(e)}
    
    async def _scrape_with_playwright(self, url: str) -> Dict[str, Any]:
        """اسکرپ با Playwright (برای صفحات JavaScript)"""
        try:
            if self.playwright is None:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(headless=True)
            
            page = await self.browser.new_page()
            
            # رفتن به صفحه
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # استخراج محتوا
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # استخراج داده‌های rendered
            title = await page.title()
            text = await page.inner_text('body')
            
            # استخراج links
            links = await page.eval_on_selector_all(
                'a[href]',
                '(elements) => elements.map(el => el.href)'
            )
            
            # استخراج images
            images = await page.eval_on_selector_all(
                'img[src]',
                '(elements) => elements.map(el => el.src)'
            )
            
            # اسکرین‌شات (اختیاری)
            # await page.screenshot(path=f'screenshot_{hash(url)}.png')
            
            await page.close()
            
            data = {
                'url': url,
                'title': title,
                'text': text,
                'links': links,
                'images': images,
                'meta': self._extract_meta_tags(soup),
                'structured_data': self._extract_structured_data(soup)
            }
            
            log.info(f"Successfully scraped {url} with playwright")
            return data
            
        except Exception as e:
            log.error(f"Error scraping {url} with playwright: {e}")
            return {'url': url, 'error': str(e)}
    
    async def _scrape_with_scrapy(self, url: str) -> Dict[str, Any]:
        """اسکرپ با Scrapy (برای crawling پیشرفته)"""
        # این متد نیاز به راه‌اندازی جداگانه Scrapy دارد
        # در اینجا یک wrapper ساده ارائه می‌شود
        
        results = []
        
        class SimpleSpider(scrapy.Spider):
            name = 'simple_spider'
            start_urls = [url]
            
            def parse(self, response: Response):
                results.append({
                    'url': response.url,
                    'status': response.status,
                    'title': response.css('title::text').get(),
                    'text': ' '.join(response.css('body ::text').getall()),
                    'links': response.css('a::attr(href)').getall(),
                    'images': response.css('img::attr(src)').getall()
                })
        
        # اجرای spider (در production باید async باشد)
        log.info(f"Scrapy scraping for {url} - use CrawlerProcess for production")
        return {'url': url, 'note': 'Use dedicated Scrapy pipeline for production'}
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """استخراج meta tags"""
        meta_tags = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content:
                meta_tags[name] = content
        
        return meta_tags
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """استخراج structured data (JSON-LD, Schema.org)"""
        structured_data = []
        
        # JSON-LD
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                structured_data.append(data)
            except:
                pass
        
        return structured_data
    
    async def scrape_multiple(self, urls: List[str], method: str = 'requests', max_concurrent: int = 5) -> List[Dict]:
        """اسکرپ چند URL به صورت همزمان"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_limit(url):
            async with semaphore:
                return await self.scrape_url(url, method)
        
        tasks = [scrape_with_limit(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # فیلتر کردن خطاها
        clean_results = []
        for result in results:
            if isinstance(result, Exception):
                log.error(f"Scraping error: {result}")
            else:
                clean_results.append(result)
        
        log.info(f"Scraped {len(clean_results)} out of {len(urls)} URLs")
        return clean_results
    
    async def extract_tables(self, url: str) -> List[pd.DataFrame]:
        """استخراج جداول HTML"""
        try:
            tables = pd.read_html(url)
            log.info(f"Extracted {len(tables)} tables from {url}")
            return tables
        except Exception as e:
            log.error(f"Error extracting tables from {url}: {e}")
            return []
    
    async def crawl_website(self, start_url: str, max_depth: int = 2, max_pages: int = 100) -> Dict[str, Any]:
        """Crawl کامل یک وبسایت"""
        
        visited = set()
        to_visit = [(start_url, 0)]  # (url, depth)
        results = []
        
        base_domain = urlparse(start_url).netloc
        
        while to_visit and len(visited) < max_pages:
            url, depth = to_visit.pop(0)
            
            if url in visited or depth > max_depth:
                continue
            
            visited.add(url)
            
            # اسکرپ صفحه
            page_data = await self.scrape_url(url, method='requests')
            results.append(page_data)
            
            # اضافه کردن لینک‌های جدید
            if 'links' in page_data and depth < max_depth:
                for link in page_data['links']:
                    # فقط لینک‌های همان دامنه
                    if urlparse(link).netloc == base_domain and link not in visited:
                        to_visit.append((link, depth + 1))
            
            # تاخیر برای جلوگیری از rate limiting
            await asyncio.sleep(1)
        
        return {
            'start_url': start_url,
            'pages_crawled': len(results),
            'max_depth': max_depth,
            'results': results
        }
    
    async def scrape_api(self, api_url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """اسکرپ از API"""
        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'url': api_url,
                'status_code': response.status_code,
                'data': data
            }
        
        except Exception as e:
            log.error(f"Error scraping API {api_url}: {e}")
            return {'url': api_url, 'error': str(e)}
    
    async def monitor_changes(self, url: str, interval: int = 3600, callback=None) -> None:
        """نظارت بر تغییرات یک صفحه"""
        previous_content = None
        
        while True:
            try:
                current_data = await self.scrape_url(url)
                current_content = current_data.get('text', '')
                
                if previous_content and current_content != previous_content:
                    log.info(f"Change detected on {url}")
                    if callback:
                        await callback(url, current_data)
                
                previous_content = current_content
                
            except Exception as e:
                log.error(f"Error monitoring {url}: {e}")
            
            await asyncio.sleep(interval)
    
    async def cleanup(self):
        """پاکسازی منابع"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

scraper = Scraper()