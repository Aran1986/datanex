import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if exists
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Upload API
export const uploadFile = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  return api.post('/upload/file', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      }
    },
  });
};

export const getFiles = async (skip = 0, limit = 50) => {
  return api.get('/upload/files', { params: { skip, limit } });
};

export const getFileInfo = async (fileId) => {
  return api.get(`/upload/file/${fileId}`);
};

export const deleteFile = async (fileId) => {
  return api.delete(`/upload/file/${fileId}`);
};

// Analysis API
export const analyzeFile = async (fileId) => {
  return api.post('/analyze/full', { file_id: fileId });
};

export const cleanData = async (fileId, strategy = 'drop') => {
  return api.post('/analyze/clean', { file_id: fileId, strategy });
};

export const deduplicateData = async (fileId, method = 'hybrid', keep = 'first') => {
  return api.post('/analyze/deduplicate', {
    file_id: fileId,
    method,
    keep,
  });
};

export const getTaskStatus = async (taskId) => {
  return api.get(`/analyze/task/${taskId}`);
};

// Scraping API
export const scrapeUrl = async (url, method = 'requests') => {
  return api.post('/scrape/url', { url, method });
};

export const scrapeMultiple = async (urls, method = 'requests', maxConcurrent = 5) => {
  return api.post('/scrape/multiple', { urls, method, max_concurrent: maxConcurrent });
};

export const crawlWebsite = async (startUrl, maxDepth = 2, maxPages = 100) => {
  return api.post('/scrape/crawl', {
    start_url: startUrl,
    max_depth: maxDepth,
    max_pages: maxPages,
  });
};

export const extractTables = async (url) => {
  return api.post('/scrape/extract-tables', null, { params: { url } });
};

// Blockchain API
export const analyzeBlockchainAddress = async (address) => {
  return api.post('/blockchain/analyze-address', { address });
};

export const getTransaction = async (txHash) => {
  return api.post('/blockchain/transaction', { tx_hash: txHash });
};

export const getBlock = async (blockNumber) => {
  return api.post('/blockchain/block', { block_number: blockNumber });
};

export const getGasPrices = async () => {
  return api.get('/blockchain/gas-prices');
};

export const analyzeContract = async (address) => {
  return api.post('/blockchain/analyze-contract', { address });
};

// Health check
export const healthCheck = async () => {
  return api.get('/health');
};

export const getStats = async () => {
  return api.get('/stats');
};

export default api;

// Location: datanex-frontend/src/services/api.js
