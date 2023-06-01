import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { JobAddEditType, JobType } from "../types";
import jobsApi from "../api/jobs";
import { getErrorMessage } from "../utils/utils";

export const useJobStore = defineStore("job", () => {
  const job = ref<JobType>();
  const jobLoading = ref<boolean>(false);
  const jobError = ref<string | null>(null);
  const jobUptime = ref<string>("");
  const jobUptimeLoading = ref<boolean>(false);
  const jobUptimeError = ref<string | null>(null);
  const jobResponseTime = ref<string>("");
  const jobResponseTimeLoading = ref<boolean>(false);
  const jobResponseTimeError = ref<string | null>(null);
  const jobStateLoading = ref<boolean>(false);

  const getJob = computed(() => job.value);
  const getJobLoading = computed(() => jobLoading.value);
  const getJobError = computed(() => jobError.value);
  const getJobUptime = computed(() => jobUptime.value);
  const getJobUptimeLoading = computed(() => jobUptimeLoading.value);
  const getJobUptimeError = computed(() => jobUptimeError.value);
  const getJobResponseTime = computed(() => jobResponseTime.value);
  const getJobResponseTimeLoading = computed(
    () => jobResponseTimeLoading.value
  );
  const getJobResponseTimeError = computed(() => jobResponseTimeError.value);
  const getJobStateLoading = computed(() => jobStateLoading.value);

  async function fetchJob(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && job.value?.uuid === uuid) {
      return;
    }

    try {
      jobLoading.value = true;

      const data = await jobsApi.getJob(uuid);
      job.value = data;

      jobError.value = null;
    } catch (err: unknown) {
      jobError.value = getErrorMessage(err);
    } finally {
      jobLoading.value = false;
    }
  }

  async function addJob(addJob: JobAddEditType): Promise<boolean> {
    let status: boolean = false;

    try {
      jobLoading.value = true;

      const data = await jobsApi.addJob(addJob);
      job.value = data;

      jobError.value = null;
      status = true;
    } catch (err: unknown) {
      jobError.value = getErrorMessage(err);
    } finally {
      jobLoading.value = false;
    }
    return status;
  }

  async function patchJob(
    uuid: string,
    patchJob: JobAddEditType
  ): Promise<boolean> {
    let status: boolean = false;
    try {
      jobLoading.value = true;

      const data = await jobsApi.patchJob(uuid, patchJob);
      job.value = data;

      jobError.value = null;
      status = true;
    } catch (err: unknown) {
      jobError.value = getErrorMessage(err);
    } finally {
      jobLoading.value = false;
    }
    return status;
  }

  async function fetchJobUptime(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && job.value?.uuid === uuid && jobUptime.value !== "") {
      return;
    }

    try {
      jobUptimeLoading.value = true;
      const data = await jobsApi.getJobUptime(uuid);
      jobUptime.value = data.uptime;
      jobUptimeError.value = null;
    } catch (err: unknown) {
      jobUptimeError.value = getErrorMessage(err);
    } finally {
      jobUptimeLoading.value = false;
    }
  }

  async function fetchJobResponseTime(
    uuid: string,
    forceLoad: boolean = false
  ) {
    if (
      !forceLoad &&
      job.value?.uuid === uuid &&
      jobResponseTime.value !== ""
    ) {
      return;
    }

    try {
      jobResponseTimeLoading.value = true;
      const data = await jobsApi.getJobResponseTime(uuid);
      jobResponseTime.value = data.response;
      jobResponseTimeError.value = null;
    } catch (err: unknown) {
      jobResponseTimeError.value = getErrorMessage(err);
    } finally {
      jobResponseTimeLoading.value = false;
    }
  }

  async function pauseJob(uuid: string) {
    try {
      jobStateLoading.value = true;
      await jobsApi.pauseJob(uuid);
      fetchJob(uuid, true);
    } catch (err: unknown) {
      console.error(err);
    } finally {
      jobStateLoading.value = false;
    }
  }

  async function resumeJob(uuid: string) {
    try {
      jobStateLoading.value = true;
      await jobsApi.resumeJob(uuid);
      fetchJob(uuid, true);
    } catch (err: unknown) {
      console.error(err);
    } finally {
      jobStateLoading.value = false;
    }
  }

  async function deleteJob(uuid: string): Promise<boolean> {
    let status: boolean = false;
    try {
      jobStateLoading.value = true;
      await jobsApi.deleteJob(uuid);
      status = true;
    } catch (err: unknown) {
      console.error(err);
      status = false;
    } finally {
      jobStateLoading.value = false;
    }

    return status;
  }

  return {
    job,
    jobLoading,
    jobError,
    jobUptime,
    jobUptimeLoading,
    jobUptimeError,
    jobResponseTime,
    jobResponseTimeLoading,
    jobResponseTimeError,
    jobStateLoading,

    getJob,
    getJobLoading,
    getJobError,
    getJobUptime,
    getJobUptimeLoading,
    getJobUptimeError,
    getJobResponseTime,
    getJobResponseTimeLoading,
    getJobResponseTimeError,
    getJobStateLoading,

    fetchJob,
    addJob,
    patchJob,
    fetchJobUptime,
    fetchJobResponseTime,
    pauseJob,
    resumeJob,
    deleteJob,
  };
});
