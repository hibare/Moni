import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { NotifierType } from "../types";
import jobsApi from "../api/jobs";
import { getErrorMessage } from "../utils/utils";

export const useJobNotifiersStore = defineStore("jobNotifiers", () => {
  const notifiers = ref<NotifierType[]>([]);
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const loadedJob = ref<string>("");

  const getNotifiers = computed(() => notifiers.value);
  const getNotifiersLoading = computed(() => loading.value);
  const getNotifiersError = computed(() => error.value);

  async function fetchNotifiers(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && loadedJob.value === uuid) {
      return;
    }

    try {
      loading.value = true;
      const data = await jobsApi.getJobNotifiers(uuid);
      notifiers.value = data;
      loadedJob.value = uuid;
      error.value = null;
    } catch (err: unknown) {
      error.value = getErrorMessage(err);
    } finally {
      loading.value = false;
    }
  }

  return {
    notifiers,
    loading,
    error,

    getNotifiers,
    getNotifiersLoading,
    getNotifiersError,

    fetchNotifiers,
  };
});
