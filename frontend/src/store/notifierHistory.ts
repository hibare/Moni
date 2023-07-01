import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { HistoryType } from "../types";
import { getErrorMessage, prettyDate } from "../utils/utils";
import notifiersApi from "../api/notifiers";

export const useNotifierHistoryStore = defineStore("notifierHistory", () => {
  const history = ref<HistoryType[]>([]);
  const historyLoading = ref<boolean>(true);
  const historyError = ref<string | null>(null);
  const loadedNotifier = ref<string>("");
  const historyDelLoading = ref<boolean>(false);
  const historyDelError = ref<string | null>(null);

  const getHistory = computed(() => history.value);
  const getHistoryLoading = computed(() => historyLoading.value);
  const getHistoryError = computed(() => historyError.value);
  const getHistoryDelLoading = computed(() => historyDelLoading.value);
  const getHistoryDelError = computed(() => historyDelError.value);

  async function fetchHistory(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && loadedNotifier.value === uuid) {
      return;
    }

    try {
      historyLoading.value = true;
      historyError.value = null;

      const data = await notifiersApi.getNotifierHistory(uuid);
      history.value = data;
      loadedNotifier.value = uuid;

      for (const hist of history.value) {
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
      historyDelError.value = null;

      await notifiersApi.deleteNotifierHistory(uuid);
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
