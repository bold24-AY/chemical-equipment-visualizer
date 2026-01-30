import React, { useState } from 'react';
import { uploadCSV } from '../services/api';

function UploadForm({ onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        setError('Please select a CSV file');
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setError('');
      setSuccess('');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      await uploadCSV(selectedFile);
      setSuccess('File uploaded and analyzed successfully!');
      setSelectedFile(null);

      // Reset file input
      const fileInput = document.getElementById('csv-file-input');
      if (fileInput) fileInput.value = '';

      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form">
      <h2>Upload Equipment Data</h2>

      <div className="file-input-wrapper">
        <input
          type="file"
          id="csv-file-input"
          accept=".csv"
          onChange={handleFileChange}
          className="file-input"
        />
        <label htmlFor="csv-file-input" className="file-input-label">
          {selectedFile ? selectedFile.name : 'Choose CSV file...'}
        </label>
      </div>

      <button
        onClick={handleUpload}
        disabled={!selectedFile || uploading}
        className="btn-primary"
      >
        {uploading ? 'Uploading...' : 'Upload & Analyze'}
      </button>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="upload-info">
        <details>
          <summary>Required columns info ⓘ</summary>
          <div className="requirements-content">
            <p>Your CSV file must contain the following columns:</p>
            <ul>
              <li>Equipment Name</li>
              <li>Type</li>
              <li>Flowrate (numeric)</li>
              <li>Pressure (numeric)</li>
              <li>Temperature (numeric)</li>
            </ul>
          </div>
        </details>
      </div>
    </div>
  );
}

export default UploadForm;
