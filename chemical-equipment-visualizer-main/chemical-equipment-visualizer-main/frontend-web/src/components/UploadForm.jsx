import React, { useState, useRef } from 'react';
import './UploadForm.css';

function UploadForm({ onUpload, loading }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
    } else {
      alert('Please select a CSV file');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file);
    } else {
      alert('Please select a CSV file');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="upload-form">
      <h2>Upload CSV File</h2>
      <form onSubmit={handleSubmit}>
        <div
          className={`drop-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleButtonClick}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            style={{ display: 'none' }}
            disabled={loading}
          />
          <div className="drop-zone-content">
            <span className="upload-icon">📁</span>
            {selectedFile ? (
              <p><strong>{selectedFile.name}</strong></p>
            ) : (
              <>
                <p>Drag and drop CSV file here</p>
                <p className="or-text">or</p>
                <button type="button" className="browse-btn">
                  Browse Files
                </button>
              </>
            )}
          </div>
        </div>

        {selectedFile && (
          <button 
            type="submit" 
            className="upload-btn"
            disabled={loading}
          >
            {loading ? 'Uploading...' : 'Upload and Process'}
          </button>
        )}
      </form>
    </div>
  );
}

export default UploadForm;