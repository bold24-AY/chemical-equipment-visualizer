import axios from 'axios';

const API_BASE_URL = '/api';

/**
 * Login user
 */
export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/login/`, {
    username,
    password,
  });
  return response.data;
};

/**
 * Logout user
 */
export const logout = async () => {
  const response = await axios.post(`${API_BASE_URL}/logout/`);
  return response.data;
};

/**
 * Check if user is authenticated
 */
export const checkAuth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/check-auth/`);
    return response.data;
  } catch (error) {
    return { authenticated: false };
  }
};

export default {
  login,
  logout,
  checkAuth,
};
