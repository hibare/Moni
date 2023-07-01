import axios, {
  InternalAxiosRequestConfig,
  AxiosResponse,
  AxiosRequestHeaders,
  AxiosError,
  AxiosRequestConfig,
} from "axios";
import router from "../router";
import { NotificationType } from "../types";
import { useAuthStore } from "../store";
import { NotifyStatus } from "../constants";
import { showNotify } from "./utils";

const requestsIgnorePaths = ["/api/v1/jobs/status/"];
const responseIgnorePaths = ["/api/v1/notifiers/test/"];
const loginPaths = ["/api/v1/accounts/jwt/"];

axios.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    if (
      config.url &&
      !requestsIgnorePaths.includes(config.url) &&
      config.url.startsWith("/api/v1/")
    ) {
      const authStore = useAuthStore();
      const token = authStore.getAccessToken.value;

      if (!config.headers) {
        config.headers = {} as AxiosRequestHeaders;
      }
      config.headers["X-Access-Token"] = `JWT ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => {
    return response;
  },
  (error: AxiosError | Error): Promise<AxiosError> => {
    if (axios.isAxiosError(error)) {
      const { method, url } = error.config as AxiosRequestConfig;
      const { status } = (error.response as AxiosResponse) ?? {};

      if (url && responseIgnorePaths.includes(url)) {
        return Promise.reject(error);
      }

      var notification = {} as NotificationType;
      const authStore = useAuthStore();

      switch (status) {
        case 400:
          notification.status = NotifyStatus.Error;
          notification.message = "Bad request";
          break;

        case 401:
          notification.status = NotifyStatus.Error;
          if (loginPaths.includes(url as string)) {
            notification.message = "Username / Password is incorrect";
          } else {
            notification.message = authStore.getIsLoggedIn.value
              ? "Session Expired"
              : "Unauthorised";
          }
          if (method === "get") {
            router.push({ name: "logout" });
          }
          break;

        case 403:
          notification.status = NotifyStatus.Error;
          notification.message = "Forbidden";
          break;

        case 404:
          notification.status = NotifyStatus.Warning;
          notification.message = "Resource not found";
          break;

        case 500:
          notification.status = NotifyStatus.Error;
          notification.message = "Internal Server Error";
          break;

        case 501:
          notification.status = NotifyStatus.Error;
          notification.message = "Not Implemented";
          break;

        case 502:
          notification.status = NotifyStatus.Error;
          notification.message = "Bad Gateway";
          break;

        case 503:
          notification.status = NotifyStatus.Error;
          notification.message = "Service Unavailable";
          break;

        case 504:
          notification.status = NotifyStatus.Error;
          notification.message = "Gateway Timeout";
          break;

        default:
          notification.status = NotifyStatus.Error;
          notification.message = "Unknown Error";
      }

      showNotify(notification);
    }
    return Promise.reject(error);
  }
);

export default axios;
