import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Upload,
  FileText,
  Globe,
  Blocks,
  Settings,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { useUIStore } from '../../store';

const Sidebar = () => {
  const { sidebarOpen, toggleSidebar } = useUIStore();

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Upload', href: '/upload', icon: Upload },
    { name: 'Scraping', href: '/scraping', icon: Globe },
    { name: 'Blockchain', href: '/blockchain', icon: Blocks },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div
      className={`fixed left-0 top-0 h-full bg-gradient-to-b from-primary-600 to-primary-800 text-white transition-all duration-300 z-50 ${
        sidebarOpen ? 'w-64' : 'w-20'
      }`}
    >
      {/* Logo */}
      <div className="flex items-center justify-between p-4 border-b border-primary-500">
        {sidebarOpen ? (
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <svg width="24" height="24" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <linearGradient id="logo-gradient-sidebar" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{stopColor:'#6366f1',stopOpacity:1}} />
                    <stop offset="100%" style={{stopColor:'#8b5cf6',stopOpacity:1}} />
                  </linearGradient>
                </defs>
                <path d="M20 2L35 11V29L20 38L5 29V11L20 2Z" stroke="url(#logo-gradient-sidebar)" strokeWidth="2" fill="none"/>
                <circle cx="20" cy="20" r="3" fill="url(#logo-gradient-sidebar)"/>
                <circle cx="14" cy="12" r="2" fill="#06b6d4"/>
                <circle cx="26" cy="12" r="2" fill="#06b6d4"/>
                <circle cx="14" cy="28" r="2" fill="#06b6d4"/>
                <circle cx="26" cy="28" r="2" fill="#06b6d4"/>
                <line x1="20" y1="20" x2="14" y2="12" stroke="url(#logo-gradient-sidebar)" strokeWidth="1.5" opacity="0.6"/>
                <line x1="20" y1="20" x2="26" y2="12" stroke="url(#logo-gradient-sidebar)" strokeWidth="1.5" opacity="0.6"/>
                <line x1="20" y1="20" x2="14" y2="28" stroke="url(#logo-gradient-sidebar)" strokeWidth="1.5" opacity="0.6"/>
                <line x1="20" y1="20" x2="26" y2="28" stroke="url(#logo-gradient-sidebar)" strokeWidth="1.5" opacity="0.6"/>
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold">DataNex</h1>
              <p className="text-xs text-primary-200">Data Analysis Platform</p>
            </div>
          </div>
        ) : (
          <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center mx-auto">
            <svg width="24" height="24" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="logo-mini" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style={{stopColor:'#6366f1',stopOpacity:1}} />
                  <stop offset="100%" style={{stopColor:'#8b5cf6',stopOpacity:1}} />
                </linearGradient>
              </defs>
              <circle cx="20" cy="20" r="8" fill="url(#logo-mini)"/>
            </svg>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="mt-8 px-3 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center ${
                sidebarOpen ? 'px-4 justify-start' : 'px-0 justify-center'
              } py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-white text-primary-600 shadow-lg'
                  : 'text-primary-100 hover:bg-primary-700 hover:text-white'
              }`
            }
          >
            <item.icon className={`${sidebarOpen ? 'mr-3' : ''} h-5 w-5`} />
            {sidebarOpen && <span className="font-medium">{item.name}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Toggle Button */}
      <button
        onClick={toggleSidebar}
        className="absolute -right-3 top-20 bg-white text-primary-600 rounded-full p-1.5 shadow-lg hover:shadow-xl transition-all duration-200"
      >
        {sidebarOpen ? (
          <ChevronLeft className="h-4 w-4" />
        ) : (
          <ChevronRight className="h-4 w-4" />
        )}
      </button>

      {/* Footer */}
      {sidebarOpen && (
        <div className="absolute bottom-4 left-0 right-0 px-4">
          <div className="bg-primary-700 rounded-lg p-3 text-sm">
            <p className="text-primary-200">Version 1.0.0</p>
            <p className="text-xs text-primary-300 mt-1">© 2024 DataNex</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;

// Location: datanex-frontend/src/components/Layout/Sidebar.jsx
