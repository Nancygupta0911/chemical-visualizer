import React from 'react';
import './DatasetHistory.css';

function DatasetHistory({ datasets, onSelect, currentDatasetId }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="dataset-history">
      <h2>Recent Datasets (Last 5)</h2>
      
      {datasets.length === 0 ? (
        <p className="no-datasets">No datasets uploaded yet. Upload a CSV to get started!</p>
      ) : (
        <div className="history-list">
          {datasets.map((dataset) => (
            <div
              key={dataset.id}
              className={`history-item ${currentDatasetId === dataset.id ? 'active' : ''}`}
              onClick={() => onSelect(dataset.id)}
            >
              <div className="history-header">
                <span className="history-filename">📁 {dataset.filename}</span>
                {currentDatasetId === dataset.id && <span className="active-badge">Active</span>}
              </div>
              <div className="history-meta">
                <span className="history-date">🕒 {formatDate(dataset.upload_date)}</span>
                <span className="history-count">
                  📊 {dataset.summary.total_count} equipment items
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DatasetHistory;