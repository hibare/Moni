import { defineStore } from "pinia";
import { ref, computed } from "vue";
import authApi from "../api/auth";
import { getErrorMessage } from "../utils/utils";

export const useAuthStore = defineStore(
  "auth",
  () => {
    const accessToken = ref<string | null>(null);
    const refreshToken = ref<string | null>(null);
    const firstName = ref<string | null>(null);
    const lastName = ref<string | null>(null);
    const email = ref<string | null>(null);
    const isLoggedIn = ref<boolean>(false);
    const isVerifyingToken = ref<boolean>(true);
    const isLoggingIn = ref<boolean>(false);

    const getAccessToken = computed(() => accessToken);
    const getRefreshToken = computed(() => refreshToken);
    const getFirstName = computed(() => firstName);
    const getLastName = computed(() => lastName);
    const getEmail = computed(() => email);
    const getIsLoggedIn = computed(() => isLoggedIn);
    const getIsVerifyingToken = computed(() => isVerifyingToken);
    const getIsLoggingIn = computed(() => isLoggingIn);

    async function login(username: string, password: string) {
      try {
        isLoggingIn.value = true;
        const data = await authApi.login(username, password);
        accessToken.value = data.access;
        refreshToken.value = data.refresh;
        firstName.value = data.firstname;
        lastName.value = data.lastname;
        email.value = data.email;
        isLoggedIn.value = true;
      } catch (err: unknown) {
        console.error(getErrorMessage(err));
      } finally {
        isLoggingIn.value = false;
      }
    }

    async function validateSession() {
      isVerifyingToken.value = true;
      if (isLoggedIn.value && accessToken.value) {
        try {
          const status = await authApi.jwtVerify(accessToken.value);

          if (!status) {
            logout();
          }
        } catch {
          logout();
        }
      } else {
        logout();
      }
      isVerifyingToken.value = false;
    }

    function logout() {
      accessToken.value = null;
      refreshToken.value = null;
      firstName.value = null;
      lastName.value = null;
      email.value = null;
      isLoggedIn.value = false;
      isVerifyingToken.value = false;
    }

    return {
      accessToken,
      refreshToken,
      firstName,
      lastName,
      email,
      isLoggedIn,
      isVerifyingToken,
      isLoggingIn,

      getAccessToken,
      getRefreshToken,
      getFirstName,
      getLastName,
      getEmail,
      getIsLoggedIn,
      getIsVerifyingToken,
      getIsLoggingIn,

      login,
      logout,
      validateSession,
    };
  },
  {
    persist: true,
  }
);
