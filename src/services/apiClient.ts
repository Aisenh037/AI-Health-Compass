import axios from 'axios';
import type { AxiosInstance, AxiosResponse, AxiosError, AxiosRequestConfig } from 'axios';

// Extend AxiosRequestConfig to include _retry
interface AxiosRequestConfigWithRetry extends AxiosRequestConfig {
  _retry?: number;
}

// Environment variables with defaults
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';
const API_TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 10000;
const MAX_RETRIES = Number(import.meta.env.VITE_MAX_RETRIES) || 3;

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error: unknown) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  async (error: AxiosError) => {
    const config = error.config as AxiosRequestConfigWithRetry;

    if (!config) {
      return Promise.reject(error);
    }

    // Retry logic for network errors
    if (error.code === 'NETWORK_ERROR' || (error.response?.status ?? 0) >= 500) {
      const retryCount = config._retry || 0;

      if (retryCount < MAX_RETRIES) {
        config._retry = retryCount + 1;
        console.log(`Retrying API call (${retryCount + 1}/${MAX_RETRIES}): ${config.url}`);

        // Exponential backoff
        const delay = Math.pow(2, retryCount) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));

        return apiClient(config);
      }
    }

    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// Generic API methods
export const api = {
  get: <T = any>(url: string, config?: any) => apiClient.get<T>(url, config),
  post: <T = any>(url: string, data?: any, config?: any) => apiClient.post<T>(url, data, config),
  put: <T = any>(url: string, data?: any, config?: any) => apiClient.put<T>(url, data, config),
  patch: <T = any>(url: string, data?: any, config?: any) => apiClient.patch<T>(url, data, config),
  delete: <T = any>(url: string, config?: any) => apiClient.delete<T>(url, config),
};

export default apiClient;
