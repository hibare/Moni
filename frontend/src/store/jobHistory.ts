import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { HistoryType } from "../types";
import jobsApi from "../api/jobs";
import { getErrorMessage, prettyDate } from "../utils/utils";

export const useJobHistoryStore = defineStore("jobHistory", () => {
  const history = ref<HistoryType[]>([]);
  const historyLoading = ref<boolean>(true);
  const historyError = ref<string | null>(null);
  const loadedJob = ref<string>("");
  const historyDelLoading = ref<boolean>(false);
  const historyDelError = ref<string | null>(null);

  const getHistory = computed(() => history.value);
  const getHistoryLoading = computed(() => historyLoading.value);
  const getHistoryError = computed(() => historyError.value);
  const getHistoryDelLoading = computed(() => historyDelLoading.value);
  const getHistoryDelError = computed(() => historyDelError.value);

  async function fetchHistory(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && loadedJob.value === uuid) {
      return;
    }

    try {
      historyLoading.value = true;
      const data = await jobsApi.getJobHistory(uuid);
      history.value = data;
      loadedJob.value = uuid;
      historyError.value = null;

      for (const hist of history.value) {
        hist.timestamp = prettyDate(hist.timestamp);
        hist.error = hist.error || "-";
      }
    } catch (err: unknown) {
      historyError.value = getErrorMessage(err);
    } finally {
      historyLoading.value = false;
    }
  }

  async function deleteHistory(uuid: string) {
    try {
      historyDelLoading.value = true;
      await jobsApi.deleteJobHistory(uuid);
      historyDelError.value = null;
      history.value = [];
    } catch (err: unknown) {
      historyDelError.value = getErrorMessage(err);
    } finally {
      historyDelLoading.value = false;
    }
  }

  return {
    history,
    historyLoading,
    historyError,
    historyDelLoading,
    historyDelError,

    getHistory,
    getHistoryLoading,
    getHistoryError,
    getHistoryDelLoading,
    getHistoryDelError,

    fetchHistory,
    deleteHistory,
  };
});
