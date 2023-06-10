import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { JobType } from "../types";
import notifierApi from "../api/notifiers";
import { getErrorMessage } from "../utils/utils";

export const useNotifierJobsStore = defineStore("notifierJobsStore", () => {
  const jobs = ref<JobType[]>([]);
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null);
  const loadedNotifier = ref<string>("");

  const getJobs = computed(() => jobs.value);
  const getJobsLoading = computed(() => loading.value);
  const getJobsError = computed(() => error.value);

  async function fetchNotifierJobs(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && loadedNotifier.value === uuid) {
      return;
    }

    try {
      loading.value = true;
      error.value = null;

      const data = await notifierApi.getNotifierJobs(uuid);
      jobs.value = data;
      loadedNotifier.value = uuid;
    } catch (err: unknown) {
      error.value = getErrorMessage(err);
    } finally {
      loading.value = false;
    }
  }

  return {
    jobs,
    loading,
    error,

    getJobs,
    getJobsError,
    getJobsLoading,

    fetchNotifierJobs,
  };
});
