import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { authMemoryStore } from "@/store/authMemoryStore";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api/v1";

export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Sends HttpOnly Secure refresh token cookie to FastAPI
  timeout: 20000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

let isRefreshing = false;
let pendingQueue: Array<{
  resolve: (token: string) => void;
  reject: (err: unknown) => void;
}> = [];

const flushQueue = (error: unknown, token: string | null = null): void => {
  pendingQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else if (token) {
      prom.resolve(token);
    }
  });
  pendingQueue = [];
};

httpClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const { accessToken, csrfToken } = authMemoryStore.getState();
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    if (csrfToken && config.headers && ["post", "put", "patch", "delete"].includes(config.method || "")) {
      config.headers["X-CSRF-Token"] = csrfToken;
    }
    return config;
  },
  (error: unknown) => Promise.reject(error)
);

httpClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      !originalRequest.url?.includes("/auth/login") &&
      !originalRequest.url?.includes("/auth/refresh")
    ) {
      if (isRefreshing) {
        return new Promise<string>((resolve, reject) => {
          pendingQueue.push({ resolve, reject });
        }).then((newToken) => {
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
          }
          return httpClient(originalRequest);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshResponse = await axios.post<{
          access_token: string;
          csrf_token: string;
        }>(
          `${API_BASE_URL}/auth/refresh`,
          {},
          { withCredentials: true }
        );

        const { access_token, csrf_token } = refreshResponse.data;
        authMemoryStore.updateAccessToken(access_token, csrf_token);
        flushQueue(null, access_token);

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
        }
        return httpClient(originalRequest);
      } catch (refreshError) {
        flushQueue(refreshError, null);
        authMemoryStore.clearSession();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);
