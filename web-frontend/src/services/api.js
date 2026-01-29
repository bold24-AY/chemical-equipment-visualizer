import axios from 'axios';

const API_BASE_URL = '/api';

// Configure axios defaults
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

/**
 * Upload CSV file to backend
 */
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_BASE_URL}/upload/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

/**
 * Get latest dataset summary
 */
export const getSummary = async () => {
  const response = await axios.get(`${API_BASE_URL}/summary/`);
  return response.data;
};

/**
 * Get upload history (last 5)
 */
export const getHistory = async () => {
  const response = await axios.get(`${API_BASE_URL}/history/`);
  return response.data;
};

/**
 * Get specific dataset by ID
 */
export const getDataset = async (datasetId) => {
  const response = await axios.get(`${API_BASE_URL}/dataset/${datasetId}/`);
  return response.data;
};

/**
 * Download PDF report
 */
export const downloadReport = async (datasetId = null) => {
  const url = datasetId 
    ? `${API_BASE_URL}/report/${datasetId}/`
    : `${API_BASE_URL}/report/`;
  
  const response = await axios.get(url, {
    responseType: 'blob',
  });
  
  // Create download link
  const blob = new Blob([response.data], { type: 'application/pdf' });
  const downloadUrl = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = downloadUrl;
  link.download = `equipment_report_${datasetId || 'latest'}.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(downloadUrl);
};

export default {
  uploadCSV,
  getSummary,
  getHistory,
  getDataset,
  downloadReport,
};
