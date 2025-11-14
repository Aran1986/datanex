# DataNex Frontend

Modern, beautiful data analysis platform built with React + Vite + TailwindCSS

## 🎨 Features

- **Modern UI/UX** - Beautiful gradient design with smooth animations
- **Drag & Drop Upload** - Easy file upload with progress tracking
- **Real-time Analysis** - Live task monitoring and status updates
- **Interactive Charts** - Data visualization with Recharts
- **Web Scraping** - Extract data from websites
- **Blockchain Analysis** - Analyze Ethereum addresses and transactions
- **Responsive Design** - Works on all devices

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
datanex-frontend/
├── src/
│   ├── components/
│   │   └── Layout/
│   │       ├── Layout.jsx
│   │       ├── Sidebar.jsx
│   │       └── Navbar.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx
│   │   ├── Upload.jsx
│   │   ├── FileDetail.jsx
│   │   ├── Scraping.jsx
│   │   ├── Blockchain.jsx
│   │   └── Settings.jsx
│   ├── services/
│   │   └── api.js
│   ├── store/
│   │   └── index.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
│   └── logo.svg
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## 🎨 Color Scheme

- **Primary**: Indigo (#6366f1) - Technology, Power
- **Secondary**: Purple (#8b5cf6) - Creativity, AI
- **Accent**: Cyan (#06b6d4) - Data, Digital

## 📝 Environment Variables

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 🔗 API Integration

The frontend connects to the BigData backend API at port 8000.

Endpoints used:
- `/upload/file` - File upload
- `/analyze/full` - Full analysis
- `/scrape/url` - Web scraping
- `/blockchain/analyze-address` - Blockchain analysis

## 🎯 Pages

### Dashboard
- Overview stats
- Activity charts  
- Recent files
- Quick actions

### Upload
- Drag & drop interface
- Progress tracking
- Auto-analysis
- File type support

### File Detail
- Analysis results
- Data preview
- Quality metrics
- Export options

### Scraping
- URL scraping
- Batch scraping
- Website crawling
- Table extraction

### Blockchain
- Address analysis
- Transaction lookup
- Block explorer
- Gas prices

### Settings
- User preferences
- API configuration
- Theme settings

## 🛠️ Technologies

- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Charts
- **Zustand** - State management
- **React Router** - Routing
- **Axios** - HTTP client
- **React Dropzone** - File upload
- **React Hot Toast** - Notifications

## 📱 Responsive Design

- **Desktop**: Full sidebar, all features
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu, optimized layout

## 🎨 Component Library

All components follow consistent design patterns:
- Buttons: `btn-primary`, `btn-secondary`
- Cards: `card`
- Inputs: `input-primary`
- Badges: `badge-success`, `badge-warning`, etc.

## 🚀 Deployment

### Build

```bash
npm run build
```

### Deploy to Vercel

```bash
vercel --prod
```

### Deploy to Netlify

```bash
netlify deploy --prod
```

## 📄 License

MIT License

## 🤝 Support

For support, email support@datanex.io
