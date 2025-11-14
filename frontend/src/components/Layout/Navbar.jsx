import React, { useState, useEffect } from 'react';
import { Bell, Search, User, Menu } from 'lucide-react';
import { useUIStore } from '../../store';
import { getStats } from '../../services/api';

const Navbar = () => {
  const toggleSidebar = useUIStore((state) => state.toggleSidebar);
  const [stats, setStats] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4 sticky top-0 z-40 shadow-sm">
      <div className="flex items-center justify-between">
        {/* Left side */}
        <div className="flex items-center space-x-4 flex-1">
          <button
            onClick={toggleSidebar}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <Menu className="h-5 w-5 text-gray-600" />
          </button>

          {/* Search */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search files, analyses..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
            />
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-6">
          {/* Stats */}
          {stats && (
            <div className="hidden md:flex items-center space-x-6 text-sm">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <span className="text-gray-600">
                  <span className="font-semibold text-gray-900">{stats.total_files}</span> Files
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-gray-600">
                  <span className="font-semibold text-gray-900">{stats.total_analyses}</span> Analyses
                </span>
              </div>
            </div>
          )}

          {/* Notifications */}
          <button className="relative p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <Bell className="h-5 w-5 text-gray-600" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User menu */}
          <div className="flex items-center space-x-3 pl-4 border-l border-gray-200">
            <div className="hidden md:block text-right">
              <p className="text-sm font-medium text-gray-900">Admin User</p>
              <p className="text-xs text-gray-500">admin@datanex.io</p>
            </div>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-semibold">
              <User className="h-5 w-5" />
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

// Location: datanex-frontend/src/components/Layout/Navbar.jsx
