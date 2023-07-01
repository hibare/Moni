import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { JobType } from "../types";
import jobsApi from "../api/jobs";
import { getErrorMessage } from "../utils/utils";

export const useJobsStore = defineStore("jobs", () => {
  const jobs = ref<JobType[]>([]);
  const loading = ref<boolean>(true);
  const error = ref<string | null>(null);

  const getJobs = computed(() => jobs.value);
  const getJobsLoading = computed(() => loading.value);
  const getJobsError = computed(() => error.value);

  async function _fetchJobs(checkPrevious: Boolean = true) {
    if (checkPrevious && jobs.value.length) {
      return;
    }

    try {
      loading.value = true;
      error.value = null;

      const data = await jobsApi.getJobs();
      jobs.value = data;
    } catch (err: unknown) {
      error.value = getErrorMessage(err);
    } finally {
      loading.value = false;
    }
  }
  async function fetchJobs() {
    await _fetchJobs();
  }

  async function forceFetchJobs() {
    await _fetchJobs(false);
  }

  return {
    jobs,
    loading,
    error,

    getJobs,
    getJobsLoading,
    getJobsError,

    fetchJobs,
    forceFetchJobs,
  };
});
