import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import UploadForm from './components/UploadForm';
import SummaryCards from './components/SummaryCards';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import { getSummary, getHistory, downloadReport } from './services/api';
import { checkAuth, logout } from './services/auth';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [history, setHistory] = useState([]);
  // Animations are now always enabled by default
  const enableAnimations = true;
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [activeTab, setActiveTab] = useState('upload');

  useEffect(() => {
    // Check authentication on mount
    const verifyAuth = async () => {
      const authStatus = await checkAuth();
      setIsAuthenticated(authStatus.authenticated);
      setLoading(false);
    };
    verifyAuth();
  }, []);

  // Use a ref to access the latest currentDataset inside loadData
  // without adding it as a dependency that triggers re-creation
  const currentDatasetRef = React.useRef(currentDataset);

  useEffect(() => {
    currentDatasetRef.current = currentDataset;
  }, [currentDataset]);

  const loadData = React.useCallback(async () => {
    try {
      if (currentDatasetRef.current) {
        setIsTransitioning(true);
        // Small delay to allow fade out
        await new Promise(resolve => setTimeout(resolve, 300));
      }

      // Try to get latest summary
      const summaryData = await getSummary();
      setCurrentDataset(summaryData);

      // Get history
      const historyData = await getHistory();
      setHistory(historyData);

      setIsTransitioning(false);
    } catch (error) {
      // No data available yet
      console.log('No data available');
      setIsTransitioning(false);
    }
  }, []); // Stable dependency array

  useEffect(() => {
    // Load data if authenticated
    if (isAuthenticated) {
      loadData();
    }
  }, [isAuthenticated, loadData]);


  const getRelativeTime = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);

    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    return date.toLocaleDateString();
  };

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    await logout();
    setIsAuthenticated(false);
    setCurrentDataset(null);
    setHistory([]);
  };

  const handleUploadSuccess = () => {
    loadData();
    setActiveTab('dashboard');
  };

  const handleDownloadReport = () => {
    downloadReport(currentDataset?.id);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧪 Chemical Equipment Visualizer</h1>
        <div className="header-actions">

          <span className="user-info">Welcome!</span>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
        </div>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-tab ${activeTab === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload
        </button>
        <button
          className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button
          className={`nav-tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📜 History
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'upload' && (
          <div className="tab-content">
            <UploadForm onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {activeTab === 'dashboard' && (
          <div className={`tab-content dashboard-content ${isTransitioning ? 'animating' : ''}`}>
            {currentDataset ? (
              <>
                <div className="dashboard-header">
                  <div>
                    <h2>Dashboard</h2>
                    <p className="dataset-info">
                      Latest upload: {currentDataset.file_name} -
                      {getRelativeTime(currentDataset.uploaded_at)}
                    </p>
                  </div>
                  <button onClick={handleDownloadReport} className="btn-primary">
                    📄 Download PDF Report
                  </button>
                </div>

                <SummaryCards summary={currentDataset.summary} enableAnimations={enableAnimations} />

                <h3 className="section-header">Visual Analysis</h3>
                <p className="dataset-info" style={{ marginBottom: '1rem' }}>
                  Showing analysis for: <strong>{currentDataset.file_name}</strong>
                </p>

                <Charts summary={currentDataset.summary} data={currentDataset.raw_data} enableAnimations={enableAnimations} />
                <DataTable data={currentDataset.raw_data} />
              </>
            ) : (
              <div className="no-data-placeholder">
                <h2>No data yet</h2>
                <p>Upload a CSV file to see visualizations.</p>
                <button onClick={() => setActiveTab('upload')} className="btn-primary">
                  Upload Data
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="tab-content">
            <h2>Upload History</h2>
            <p className="subtitle">Last 5 uploads</p>

            {history.length > 0 ? (
              <div className="history-list">
                {history.map((dataset) => (
                  <div key={dataset.id} className="history-item">
                    <div className="history-info">
                      <h3>{dataset.file_name}</h3>
                      <p>{getRelativeTime(dataset.uploaded_at)}</p>
                      <p className="equipment-count">
                        {dataset.summary.total_equipment} equipment items
                      </p>
                    </div>
                    <div className="history-actions">
                      <button
                        onClick={() => downloadReport(dataset.id)}
                        className="btn-primary"
                        style={{ width: 'auto', padding: '0.5rem 1rem' }}
                      >
                        Download PDF
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No upload history available.</div>
            )}
          </div>
        )}
      </main>


      <footer className="app-footer">
        <p>Chemical Equipment Parameter Visualizer © 2026</p>
      </footer>
    </div>
  );
}

export default App;
