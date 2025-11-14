import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload as UploadIcon, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadFile, analyzeFile } from '../../services/api';
import { useFileStore } from '../../store';
import toast from 'react-hot-toast';

const Upload = () => {
  const [uploadingFiles, setUploadingFiles] = useState([]);
  const addFile = useFileStore((state) => state.addFile);

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach(file => handleUpload(file));
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/json': ['.json'],
      'application/xml': ['.xml'],
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
    },
    maxSize: 500 * 1024 * 1024, // 500MB
  });

  const handleUpload = async (file) => {
    const uploadId = Date.now();
    
    setUploadingFiles(prev => [...prev, {
      id: uploadId,
      file,
      progress: 0,
      status: 'uploading',
      error: null
    }]);

    try {
      const response = await uploadFile(file, (progress) => {
        setUploadingFiles(prev =>
          prev.map(f => f.id === uploadId ? { ...f, progress } : f)
        );
      });

      setUploadingFiles(prev =>
        prev.map(f => f.id === uploadId ? { ...f, status: 'analyzing', progress: 100 } : f)
      );

      // Auto-analyze
      await analyzeFile(response.data.file_id);

      addFile(response.data);
      
      setUploadingFiles(prev =>
        prev.map(f => f.id === uploadId ? { ...f, status: 'success' } : f)
      );

      toast.success(`${file.name} uploaded successfully!`);

      // Remove from list after 3 seconds
      setTimeout(() => {
        setUploadingFiles(prev => prev.filter(f => f.id !== uploadId));
      }, 3000);

    } catch (error) {
      console.error('Upload failed:', error);
      setUploadingFiles(prev =>
        prev.map(f => f.id === uploadId ? {
          ...f,
          status: 'error',
          error: error.response?.data?.detail || 'Upload failed'
        } : f)
      );
      toast.error(`Failed to upload ${file.name}`);
    }
  };

  const removeUploadingFile = (id) => {
    setUploadingFiles(prev => prev.filter(f => f.id !== id));
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Upload Files</h1>
        <p className="text-gray-600 mt-1">Upload and analyze your data files</p>
      </div>

      {/* Upload Zone */}
      <div className="card">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 cursor-pointer ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center">
            <div className={`p-4 rounded-full mb-4 ${
              isDragActive ? 'bg-primary-100' : 'bg-gray-100'
            }`}>
              <UploadIcon className={`h-12 w-12 ${
                isDragActive ? 'text-primary-600' : 'text-gray-400'
              }`} />
            </div>
            
            {isDragActive ? (
              <p className="text-lg font-medium text-primary-600">
                Drop your files here...
              </p>
            ) : (
              <>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  Drag & drop files here, or click to select
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  Supports: CSV, Excel, JSON, XML, PDF, TXT (Max 500MB)
                </p>
                <button className="btn-primary">
                  Choose Files
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Uploading Files */}
      {uploadingFiles.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Uploading Files</h3>
          <div className="space-y-3">
            {uploadingFiles.map((upload) => (
              <div key={upload.id} className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-3">
                    <File className="h-5 w-5 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{upload.file.name}</p>
                      <p className="text-xs text-gray-500">
                        {(upload.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {upload.status === 'success' && (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    )}
                    {upload.status === 'error' && (
                      <AlertCircle className="h-5 w-5 text-red-500" />
                    )}
                    <button
                      onClick={() => removeUploadingFile(upload.id)}
                      className="p-1 hover:bg-gray-200 rounded transition-colors"
                    >
                      <X className="h-4 w-4 text-gray-500" />
                    </button>
                  </div>
                </div>

                {upload.status === 'uploading' && (
                  <>
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${upload.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-500">Uploading... {upload.progress}%</p>
                  </>
                )}

                {upload.status === 'analyzing' && (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                    <p className="text-xs text-gray-600">Analyzing data...</p>
                  </div>
                )}

                {upload.status === 'success' && (
                  <p className="text-xs text-green-600">✓ Upload complete!</p>
                )}

                {upload.status === 'error' && (
                  <p className="text-xs text-red-600">✗ {upload.error}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-blue-100 p-2 rounded-lg">
              <File className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Automatic Analysis</h4>
              <p className="text-sm text-gray-600">
                Files are automatically analyzed after upload including categorization, validation, and pattern detection.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-purple-100 p-2 rounded-lg">
              <CheckCircle className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Quality Check</h4>
              <p className="text-sm text-gray-600">
                Detect duplicate records, validate data quality, and identify issues automatically.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-start space-x-3">
            <div className="bg-green-100 p-2 rounded-lg">
              <UploadIcon className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-1">Large Files</h4>
              <p className="text-sm text-gray-600">
                Support for files up to 500MB with efficient processing and background tasks.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Supported Formats */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Supported File Formats</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'CSV', desc: 'Comma-separated values', icon: '📊' },
            { name: 'Excel', desc: 'XLSX, XLS files', icon: '📈' },
            { name: 'JSON', desc: 'JavaScript Object Notation', icon: '{ }' },
            { name: 'XML', desc: 'Extensible Markup Language', icon: '<>' },
            { name: 'PDF', desc: 'Portable Document Format', icon: '📄' },
            { name: 'TXT', desc: 'Plain text files', icon: '📝' },
            { name: 'Parquet', desc: 'Columnar storage', icon: '🗂️' },
            { name: 'SQL', desc: 'SQL dump files', icon: '🗄️' },
          ].map((format) => (
            <div key={format.name} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
              <span className="text-2xl">{format.icon}</span>
              <div>
                <p className="font-medium text-gray-900">{format.name}</p>
                <p className="text-xs text-gray-500">{format.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Upload;

// Location: datanex-frontend/src/pages/Upload.jsx
