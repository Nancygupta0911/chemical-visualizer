import React from 'react';
import './Summary.css';

function Summary({ summary, filename, onDownloadPDF }) {
  return (
    <div className="summary-container">
      <div className="summary-header">
        <h2>Summary Statistics</h2>
        <button className="pdf-btn" onClick={onDownloadPDF}>
          📄 Download PDF Report
        </button>
      </div>
      
      <div className="summary-filename">
        <strong>Dataset:</strong> {filename}
      </div>

      <div className="summary-grid">
        <div className="summary-card">
          <div className="card-icon">📊</div>
          <div className="card-content">
            <h3>Total Equipment</h3>
            <p className="card-value">{summary.total_count}</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="card-icon">💧</div>
          <div className="card-content">
            <h3>Avg Flowrate</h3>
            <p className="card-value">{summary.avg_flowrate.toFixed(2)}</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="card-icon">⚡</div>
          <div className="card-content">
            <h3>Avg Pressure</h3>
            <p className="card-value">{summary.avg_pressure.toFixed(2)}</p>
          </div>
        </div>

        <div className="summary-card">
          <div className="card-icon">🌡️</div>
          <div className="card-content">
            <h3>Avg Temperature</h3>
            <p className="card-value">{summary.avg_temperature.toFixed(2)}</p>
          </div>
        </div>
      </div>

      <div className="type-distribution">
        <h3>Equipment Type Distribution</h3>
        <div className="type-list">
          {Object.entries(summary.type_distribution).map(([type, count]) => (
            <div key={type} className="type-item">
              <span className="type-name">{type}</span>
              <span className="type-count">{count} units</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Summary;