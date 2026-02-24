import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // Assuming Django is running on port 8000 locally
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

/* Optional Response Interceptor to handle Refresh Logic (can be added later if needed)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
      // Logic for token refresh
  }
);
*/

export default api;
