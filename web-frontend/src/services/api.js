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
  try {
    const url = datasetId
      ? `${API_BASE_URL}/report/${datasetId}/`
      : `${API_BASE_URL}/report/`;

    console.log(`Downloading report for datasetId: ${datasetId || 'latest'}`);

    const response = await axios.get(url, {
      responseType: 'blob',
    });

    // Check if response is actually a JSON error masquerading as a blob
    if (response.data.type === 'application/json') {
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const errorData = JSON.parse(reader.result);
          console.error("PDF Download Error (JSON):", errorData);
          alert(`Failed to download PDF: ${errorData.error || 'Unknown server error'}`);
        } catch (e) {
          alert('Failed to download PDF: Server returned an error.');
        }
      };
      reader.readAsText(response.data);
      return;
    }

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

  } catch (error) {
    console.error("PDF Download Error:", error);
    if (error.response && error.response.data instanceof Blob) {
      // Try to read blob error
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const errorData = JSON.parse(reader.result);
          alert(`Error: ${errorData.error || error.message}`);
        } catch (e) {
          alert(`Error: ${error.message}`);
        }
      };
      reader.readAsText(error.response.data);
    } else {
      alert(`Failed to download report: ${error.message}`);
    }
  }
};

export default {
  uploadCSV,
  getSummary,
  getHistory,
  getDataset,
  downloadReport,
};
