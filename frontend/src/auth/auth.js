// frontend/src/auth/auth.js

const TOKEN_KEY = "access_token";

/**
 * Save JWT token after successful login
 * @param {string} token
 */
export const setToken = (token) => {
  if (!token) return;
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Get stored JWT token
 * @returns {string | null}
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Remove token on logout
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Check if user is authenticated
 * @returns {boolean}
 */
export const isAuthenticated = () => {
  const token = localStorage.getItem(TOKEN_KEY);
  return Boolean(token);
};
