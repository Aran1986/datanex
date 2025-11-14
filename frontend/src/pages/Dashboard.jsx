import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Upload,
  FileText,
  Globe,
  Blocks,
  TrendingUp,
  Activity,
  Clock,
  CheckCircle,
} from 'lucide-react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { getFiles, getStats } from '../../services/api';
import toast from 'react-hot-toast';

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentFiles, setRecentFiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [statsRes, filesRes] = await Promise.all([
        getStats(),
        getFiles(0, 5)
      ]);
      
      setStats(statsRes.data);
      setRecentFiles(filesRes.data.files);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  // Mock data for charts
  const activityData = [
    { name: 'Mon', uploads: 12, analyses: 8 },
    { name: 'Tue', uploads: 19, analyses: 15 },
    { name: 'Wed', uploads: 15, analyses: 12 },
    { name: 'Thu', uploads: 25, analyses: 20 },
    { name: 'Fri', uploads: 22, analyses: 18 },
    { name: 'Sat', uploads: 10, analyses: 7 },
    { name: 'Sun', uploads: 8, analyses: 5 },
  ];

  const fileTypeData = [
    { name: 'CSV', value: 45, color: '#6366f1' },
    { name: 'Excel', value: 30, color: '#8b5cf6' },
    { name: 'JSON', value: 15, color: '#06b6d4' },
    { name: 'PDF', value: 10, color: '#10b981' },
  ];

  const statCards = [
    {
      title: 'Total Files',
      value: stats?.total_files || 0,
      icon: FileText,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'increase'
    },
    {
      title: 'Analyses',
      value: stats?.total_analyses || 0,
      icon: Activity,
      color: 'bg-purple-500',
      change: '+8%',
      changeType: 'increase'
    },
    {
      title: 'Active Tasks',
      value: stats?.total_tasks || 0,
      icon: Clock,
      color: 'bg-amber-500',
      change: '3 running',
      changeType: 'neutral'
    },
    {
      title: 'Completed',
      value: '95%',
      icon: CheckCircle,
      color: 'bg-green-500',
      change: '+5%',
      changeType: 'increase'
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back! Here's what's happening with your data.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <div
            key={index}
            className="card hover:scale-105 transition-transform duration-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 font-medium">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                <div className="flex items-center mt-2 space-x-1">
                  <TrendingUp className={`h-4 w-4 ${stat.changeType === 'increase' ? 'text-green-500' : 'text-gray-400'}`} />
                  <span className={`text-sm ${stat.changeType === 'increase' ? 'text-green-600' : 'text-gray-600'}`}>
                    {stat.change}
                  </span>
                </div>
              </div>
              <div className={`${stat.color} p-4 rounded-xl`}>
                <stat.icon className="h-8 w-8 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          onClick={() => navigate('/upload')}
          className="card hover:shadow-xl transition-all duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-3 rounded-lg group-hover:scale-110 transition-transform">
              <Upload className="h-6 w-6 text-white" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-gray-900">Upload File</p>
              <p className="text-sm text-gray-500">Analyze your data</p>
            </div>
          </div>
        </button>

        <button
          onClick={() => navigate('/scraping')}
          className="card hover:shadow-xl transition-all duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-br from-accent-500 to-accent-600 p-3 rounded-lg group-hover:scale-110 transition-transform">
              <Globe className="h-6 w-6 text-white" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-gray-900">Web Scraping</p>
              <p className="text-sm text-gray-500">Extract web data</p>
            </div>
          </div>
        </button>

        <button
          onClick={() => navigate('/blockchain')}
          className="card hover:shadow-xl transition-all duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-br from-secondary-500 to-secondary-600 p-3 rounded-lg group-hover:scale-110 transition-transform">
              <Blocks className="h-6 w-6 text-white" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-gray-900">Blockchain</p>
              <p className="text-sm text-gray-500">Analyze addresses</p>
            </div>
          </div>
        </button>

        <button className="card hover:shadow-xl transition-all duration-200 group">
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-br from-green-500 to-green-600 p-3 rounded-lg group-hover:scale-110 transition-transform">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <div className="text-left">
              <p className="font-semibold text-gray-900">View Reports</p>
              <p className="text-sm text-gray-500">See all analyses</p>
            </div>
          </div>
        </button>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Chart */}
        <div className="lg:col-span-2 card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Activity Overview</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={activityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#fff', 
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
              />
              <Bar dataKey="uploads" fill="#6366f1" radius={[8, 8, 0, 0]} />
              <Bar dataKey="analyses" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* File Types Pie Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">File Types</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={fileTypeData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {fileTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {fileTypeData.map((item, index) => (
              <div key={index} className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span className="text-sm text-gray-600">{item.name}</span>
                </div>
                <span className="text-sm font-semibold text-gray-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Files */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Recent Files</h3>
          <button 
            onClick={() => navigate('/upload')}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            View all →
          </button>
        </div>
        
        <div className="space-y-3">
          {recentFiles.length > 0 ? (
            recentFiles.map((file) => (
              <div
                key={file.file_id}
                onClick={() => navigate(`/files/${file.file_id}`)}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="bg-primary-100 p-2 rounded-lg">
                    <FileText className="h-5 w-5 text-primary-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{file.filename}</p>
                    <p className="text-sm text-gray-500">
                      {new Date(file.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <span className={`badge ${
                  file.status === 'completed' ? 'badge-success' :
                  file.status === 'processing' ? 'badge-warning' :
                  'badge-info'
                }`}>
                  {file.status}
                </span>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-2 text-gray-400" />
              <p>No files yet. Upload your first file to get started!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

// Location: datanex-frontend/src/pages/Dashboard.jsx
