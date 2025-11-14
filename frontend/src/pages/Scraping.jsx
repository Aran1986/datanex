import React, { useState } from 'react';
import {
  Globe,
  Link as LinkIcon,
  Search,
  Download,
  AlertCircle,
  CheckCircle,
  Loader,
} from 'lucide-react';
import { scrapeUrl, scrapeMultiple, crawlWebsite, extractTables } from '../services/api';
import toast from 'react-hot-toast';

const Scraping = () => {
  const [activeTab, setActiveTab] = useState('single');
  const [singleUrl, setSingleUrl] = useState('');
  const [multipleUrls, setMultipleUrls] = useState('');
  const [crawlUrl, setCrawlUrl] = useState('');
  const [maxDepth, setMaxDepth] = useState(2);
  const [maxPages, setMaxPages] = useState(100);
  const [method, setMethod] = useState('requests');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSingleScrape = async () => {
    if (!singleUrl) {
      toast.error('Please enter a URL');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await scrapeUrl(singleUrl, method);
      setResult(response.data);
      toast.success('Scraping completed successfully!');
    } catch (error) {
      console.error('Scraping failed:', error);
      toast.error(error.response?.data?.detail || 'Scraping failed');
    } finally {
      setLoading(false);
    }
  };

  const handleMultipleScrape = async () => {
    const urls = multipleUrls.split('\n').filter(url => url.trim());
    
    if (urls.length === 0) {
      toast.error('Please enter at least one URL');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await scrapeMultiple(urls, method);
      setResult(response.data);
      toast.success(`Scraped ${urls.length} URLs successfully!`);
    } catch (error) {
      console.error('Multiple scraping failed:', error);
      toast.error(error.response?.data?.detail || 'Scraping failed');
    } finally {
      setLoading(false);
    }
  };

  const handleCrawl = async () => {
    if (!crawlUrl) {
      toast.error('Please enter a starting URL');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await crawlWebsite(crawlUrl, maxDepth, maxPages);
      setResult(response.data);
      toast.success('Website crawling completed!');
    } catch (error) {
      console.error('Crawling failed:', error);
      toast.error(error.response?.data?.detail || 'Crawling failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExtractTables = async () => {
    if (!singleUrl) {
      toast.error('Please enter a URL');
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await extractTables(singleUrl);
      setResult(response.data);
      toast.success('Tables extracted successfully!');
    } catch (error) {
      console.error('Table extraction failed:', error);
      toast.error(error.response?.data?.detail || 'Extraction failed');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'single', name: 'Single URL', icon: LinkIcon },
    { id: 'multiple', name: 'Multiple URLs', icon: Search },
    { id: 'crawl', name: 'Website Crawl', icon: Globe },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Web Scraping</h1>
        <p className="text-gray-600 mt-1">Extract data from websites efficiently</p>
      </div>

      {/* Tabs */}
      <div className="card">
        <div className="flex space-x-2 border-b border-gray-200 pb-4">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-primary-500 text-white shadow-lg'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.name}</span>
            </button>
          ))}
        </div>

        {/* Single URL Tab */}
        {activeTab === 'single' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URL to Scrape
              </label>
              <input
                type="url"
                value={singleUrl}
                onChange={(e) => setSingleUrl(e.target.value)}
                placeholder="https://example.com"
                className="input-primary"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Scraping Method
              </label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="input-primary"
              >
                <option value="requests">Requests (Fast)</option>
                <option value="playwright">Playwright (JavaScript support)</option>
                <option value="scrapy">Scrapy (Advanced)</option>
              </select>
            </div>

            <div className="flex space-x-4">
              <button
                onClick={handleSingleScrape}
                disabled={loading}
                className="btn-primary flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <Loader className="h-4 w-4 animate-spin" />
                    <span>Scraping...</span>
                  </>
                ) : (
                  <>
                    <Globe className="h-4 w-4" />
                    <span>Start Scraping</span>
                  </>
                )}
              </button>

              <button
                onClick={handleExtractTables}
                disabled={loading}
                className="btn-secondary flex items-center space-x-2"
              >
                <Download className="h-4 w-4" />
                <span>Extract Tables</span>
              </button>
            </div>
          </div>
        )}

        {/* Multiple URLs Tab */}
        {activeTab === 'multiple' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URLs (one per line)
              </label>
              <textarea
                value={multipleUrls}
                onChange={(e) => setMultipleUrls(e.target.value)}
                placeholder="https://example.com/page1&#10;https://example.com/page2&#10;https://example.com/page3"
                rows={8}
                className="input-primary font-mono text-sm"
              />
              <p className="text-xs text-gray-500 mt-1">
                Enter one URL per line. Maximum 100 URLs.
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Scraping Method
              </label>
              <select
                value={method}
                onChange={(e) => setMethod(e.target.value)}
                className="input-primary"
              >
                <option value="requests">Requests (Fast)</option>
                <option value="playwright">Playwright (JavaScript support)</option>
                <option value="scrapy">Scrapy (Advanced)</option>
              </select>
            </div>

            <button
              onClick={handleMultipleScrape}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Scraping...</span>
                </>
              ) : (
                <>
                  <Search className="h-4 w-4" />
                  <span>Scrape Multiple URLs</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Website Crawl Tab */}
        {activeTab === 'crawl' && (
          <div className="mt-6 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Starting URL
              </label>
              <input
                type="url"
                value={crawlUrl}
                onChange={(e) => setCrawlUrl(e.target.value)}
                placeholder="https://example.com"
                className="input-primary"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Depth
                </label>
                <input
                  type="number"
                  value={maxDepth}
                  onChange={(e) => setMaxDepth(parseInt(e.target.value))}
                  min="1"
                  max="5"
                  className="input-primary"
                />
                <p className="text-xs text-gray-500 mt-1">
                  How many levels deep to crawl (1-5)
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Pages
                </label>
                <input
                  type="number"
                  value={maxPages}
                  onChange={(e) => setMaxPages(parseInt(e.target.value))}
                  min="1"
                  max="1000"
                  className="input-primary"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Maximum number of pages to scrape
                </p>
              </div>
            </div>

            <button
              onClick={handleCrawl}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  <span>Crawling...</span>
                </>
              ) : (
                <>
                  <Globe className="h-4 w-4" />
                  <span>Start Crawling</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Results</h3>
            <CheckCircle className="h-6 w-6 text-green-500" />
          </div>

          <div className="bg-gray-50 rounded-lg p-4 overflow-auto max-h-96">
            <pre className="text-sm text-gray-800">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Globe className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Multiple Methods</h4>
              <p className="text-sm text-gray-600">
                Choose between Requests, Playwright, or Scrapy based on your needs.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-purple-100 p-2 rounded-lg">
              <Search className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Batch Processing</h4>
              <p className="text-sm text-gray-600">
                Scrape multiple URLs concurrently for faster data collection.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-green-100 p-2 rounded-lg">
              <Download className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Table Extraction</h4>
              <p className="text-sm text-gray-600">
                Automatically extract and parse HTML tables from web pages.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Scraping;

// Location: datanex-frontend/src/pages/Scraping.jsx
