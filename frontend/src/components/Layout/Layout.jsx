import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { useUIStore } from '../../store';

const Layout = () => {
  const sidebarOpen = useUIStore((state) => state.sidebarOpen);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      
      <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
        <Navbar />
        
        <main className="flex-1 overflow-y-auto bg-gradient-to-br from-gray-50 to-gray-100 p-6">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;

// Location: datanex-frontend/src/components/Layout/Layout.jsx
