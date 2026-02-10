import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import UploadForm from './components/UploadForm';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import Summary from './components/Summary';
import DatasetHistory from './components/DatasetHistory';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
      setIsAuthenticated(true);
      setUser({ username });
      fetchDatasets();
    }
  }, []);

  const handleLogin = (userData) => {
    setIsAuthenticated(true);
    setUser(userData);
    fetchDatasets();
  };

  const handleLogout = async () => {
    try {
      await axios.post(`${API_BASE_URL}/auth/logout/`);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      delete axios.defaults.headers.common['Authorization'];
      setIsAuthenticated(false);
      setUser(null);
      setCurrentDataset(null);
      setDatasets([]);
    }
  };

  const fetchDatasets = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets/`);
      setDatasets(response.data);
    } catch (err) {
      console.error('Error fetching datasets:', err);
    }
  };

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/datasets/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setCurrentDataset(response.data);
      fetchDatasets();
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
      setLoading(false);
    }
  };

  const handleSelectDataset = async (datasetId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets/${datasetId}/`);
      setCurrentDataset(response.data);
    } catch (err) {
      console.error('Error fetching dataset:', err);
    }
  };

  const handleDownloadPDF = async (datasetId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/datasets/${datasetId}/download_pdf/`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${datasetId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Error downloading PDF:', err);
    }
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>⚗️ Chemical Equipment Parameter Visualizer</h1>
        <div className="header-right">
          <span>Welcome, {user?.username}!</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="App-main">
        <div className="container">
          <section className="upload-section">
            <UploadForm onUpload={handleUpload} loading={loading} />
            {error && <div className="error-message">{error}</div>}
          </section>

          {currentDataset && (
            <>
              <section className="summary-section">
                <Summary 
                  summary={currentDataset.summary} 
                  filename={currentDataset.filename}
                  onDownloadPDF={() => handleDownloadPDF(currentDataset.id)}
                />
              </section>

              <section className="charts-section">
                <Charts data={currentDataset.data} summary={currentDataset.summary} />
              </section>

              <section className="table-section">
                <DataTable data={currentDataset.data} />
              </section>
            </>
          )}

          <section className="history-section">
            <DatasetHistory 
              datasets={datasets} 
              onSelect={handleSelectDataset}
              currentDatasetId={currentDataset?.id}
            />
          </section>
        </div>
      </main>

      <footer className="App-footer">
        <p>Chemical Equipment Parameter Visualizer © 2026</p>
      </footer>
    </div>
  );
}

export default App;