import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  FileText,
  Download,
  Trash2,
  AlertCircle,
  CheckCircle,
  Clock,
  Database,
  BarChart3,
  ArrowLeft,
} from 'lucide-react';
import { getFileInfo, deleteFile } from '../services/api';
import toast from 'react-hot-toast';

const FileDetail = () => {
  const { fileId } = useParams();
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFileDetail();
  }, [fileId]);

  const loadFileDetail = async () => {
    try {
      setLoading(true);
      const response = await getFileInfo(fileId);
      setFile(response.data);
    } catch (error) {
      console.error('Failed to load file:', error);
      toast.error('Failed to load file details');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this file?')) {
      return;
    }

    try {
      await deleteFile(fileId);
      toast.success('File deleted successfully');
      navigate('/upload');
    } catch (error) {
      console.error('Failed to delete file:', error);
      toast.error('Failed to delete file');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!file) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-gray-900 mb-2">File not found</h3>
        <p className="text-gray-600 mb-4">The file you're looking for doesn't exist.</p>
        <button onClick={() => navigate('/upload')} className="btn-primary">
          Back to Upload
        </button>
      </div>
    );
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const getStatusBadge = (status) => {
    const badges = {
      'uploaded': { class: 'badge-info', icon: Clock },
      'processing': { class: 'badge-warning', icon: Clock },
      'completed': { class: 'badge-success', icon: CheckCircle },
      'failed': { class: 'badge-error', icon: AlertCircle },
    };
    const badge = badges[status] || badges.uploaded;
    const Icon = badge.icon;
    
    return (
      <span className={`badge ${badge.class} flex items-center space-x-1`}>
        <Icon className="h-3 w-3" />
        <span>{status}</span>
      </span>
    );
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/upload')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-5 w-5 text-gray-600" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">File Details</h1>
            <p className="text-gray-600 mt-1">View and manage your file</p>
          </div>
        </div>
        <button
          onClick={handleDelete}
          className="flex items-center space-x-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors"
        >
          <Trash2 className="h-4 w-4" />
          <span>Delete</span>
        </button>
      </div>

      {/* File Info Card */}
      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center space-x-4">
            <div className="bg-primary-100 p-4 rounded-xl">
              <FileText className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">{file.filename}</h2>
              <p className="text-gray-600 mt-1">
                Uploaded on {new Date(file.created_at).toLocaleString()}
              </p>
            </div>
          </div>
          {getStatusBadge(file.status)}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <Database className="h-5 w-5 text-gray-600" />
              <p className="text-sm font-medium text-gray-600">File Size</p>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {formatFileSize(file.file_size)}
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <FileText className="h-5 w-5 text-gray-600" />
              <p className="text-sm font-medium text-gray-600">File Type</p>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {file.file_type.toUpperCase()}
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <BarChart3 className="h-5 w-5 text-gray-600" />
              <p className="text-sm font-medium text-gray-600">Rows</p>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {file.metadata?.row_count?.toLocaleString() || 'N/A'}
            </p>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <BarChart3 className="h-5 w-5 text-gray-600" />
              <p className="text-sm font-medium text-gray-600">Columns</p>
            </div>
            <p className="text-2xl font-bold text-gray-900">
              {file.metadata?.column_count || 'N/A'}
            </p>
          </div>
        </div>
      </div>

      {/* Metadata */}
      {file.metadata && Object.keys(file.metadata).length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Additional Information</h3>
          <div className="bg-gray-50 rounded-lg p-4 overflow-auto">
            <pre className="text-sm text-gray-800">
              {JSON.stringify(file.metadata, null, 2)}
            </pre>
          </div>
        </div>
      )}

      {/* Analysis Results */}
      {file.analysis_results && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Analysis Results</h3>
          <div className="space-y-4">
            {file.analysis_results.categories && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Categories</h4>
                <div className="flex flex-wrap gap-2">
                  {file.analysis_results.categories.map((category, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-primary-100 text-primary-800 rounded-full text-sm font-medium"
                    >
                      {category}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {file.analysis_results.quality_score && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Data Quality</h4>
                <div className="flex items-center space-x-4">
                  <div className="flex-1 bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-gradient-to-r from-green-500 to-green-600 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${file.analysis_results.quality_score}%` }}
                    ></div>
                  </div>
                  <span className="text-lg font-bold text-gray-900">
                    {file.analysis_results.quality_score}%
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
        <div className="flex flex-wrap gap-4">
          <button className="btn-primary flex items-center space-x-2">
            <Download className="h-4 w-4" />
            <span>Download File</span>
          </button>
          <button className="btn-secondary flex items-center space-x-2">
            <BarChart3 className="h-4 w-4" />
            <span>Re-analyze</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default FileDetail;

// Location: datanex-frontend/src/pages/FileDetail.jsx
