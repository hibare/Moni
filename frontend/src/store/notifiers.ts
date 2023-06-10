import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { NotifierType } from "../types";
import notifiersApi from "../api/notifiers";
import { getErrorMessage } from "../utils/utils";

export const useNotifiersStore = defineStore("notifiersStore", () => {
  const notifiers = ref<NotifierType[]>([]);
  const loading = ref<boolean>(true);
  const error = ref<string | null>(null);

  const getNotifiers = computed(() => notifiers.value);
  const getNotifiersLoading = computed(() => loading.value);
  const getNotifiersError = computed(() => error.value);

  async function _fetchNotifiers(checkPrevious: Boolean = true) {
    if (checkPrevious && notifiers.value.length) {
      return;
    }

    try {
      loading.value = true;
      error.value = null;

      const data = await notifiersApi.getNotifiers();
      notifiers.value = data;
    } catch (err: unknown) {
      error.value = getErrorMessage(err);
    } finally {
      loading.value = false;
    }
  }

  async function fetchNotifiers() {
    await _fetchNotifiers();
  }

  async function forceFetchNotifiers() {
    await _fetchNotifiers(false);
  }

  return {
    notifiers,
    loading,
    error,

    getNotifiers,
    getNotifiersLoading,
    getNotifiersError,

    fetchNotifiers,
    forceFetchNotifiers,
  };
});
