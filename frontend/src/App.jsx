import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Upload from './pages/Upload';
import FileDetail from './pages/FileDetail';
import Scraping from './pages/Scraping';
import Blockchain from './pages/Blockchain';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#fff',
              color: '#374151',
              boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)',
            },
            success: {
              iconTheme: {
                primary: '#10b981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
        
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="upload" element={<Upload />} />
            <Route path="files/:fileId" element={<FileDetail />} />
            <Route path="scraping" element={<Scraping />} />
            <Route path="blockchain" element={<Blockchain />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;

// Location: datanex-frontend/src/App.jsx
