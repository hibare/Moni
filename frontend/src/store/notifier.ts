import { computed, ref } from "vue";
import { defineStore } from "pinia";
import { NotifierAddEditType, NotifierType } from "../types";
import notifiersApi from "../api/notifiers";
import { getErrorMessage } from "../utils/utils";

export const useNotifierStore = defineStore("notifierStore", () => {
  const notifier = ref<NotifierType>();
  const notifierLoading = ref<boolean>(false);
  const notifierError = ref<string | null>(null);
  const notifierDelivery = ref<string>("");
  const notifierDeliveryLoading = ref<boolean>(false);
  const notifierDeliveryError = ref<string | null>(null);
  const notifierTestLoading = ref<boolean>(false);
  const notifierStateLoading = ref<boolean>(false);

  const getNotifier = computed(() => notifier.value);
  const getNotifierLoading = computed(() => notifierLoading.value);
  const getNotifierError = computed(() => notifierError.value);
  const getNotifierDelivery = computed(() => notifierDelivery.value);
  const getNotifierDeliveryLoading = computed(
    () => notifierDeliveryLoading.value
  );
  const getNotifierDeliveryError = computed(() => notifierDeliveryError.value);
  const getNotifierTestLoading = computed(() => notifierTestLoading.value);
  const getNotifierStateLoading = computed(() => notifierStateLoading.value);

  async function fetchNotifier(uuid: string, forceLoad: boolean = false) {
    if (!forceLoad && notifier.value?.uuid === uuid) {
      return;
    }

    try {
      notifierLoading.value = true;
      notifierError.value = null;

      const data = await notifiersApi.getNotifier(uuid);
      notifier.value = data;
    } catch (err: unknown) {
      notifierError.value = getErrorMessage(err);
    } finally {
      notifierLoading.value = false;
    }
  }

  async function addNotifier(
    addNotifier: NotifierAddEditType
  ): Promise<boolean> {
    let status: boolean = false;

    try {
      notifierLoading.value = true;

      const data = await notifiersApi.addNotifier(addNotifier);
      notifier.value = data;
      notifierError.value = null;
      status = true;
    } catch (err: unknown) {
      notifierError.value = getErrorMessage(err);
    } finally {
      notifierLoading.value = false;
    }
    return status;
  }

  async function patchNotifier(
    uuid: string,
    patchNotifier: NotifierAddEditType
  ): Promise<boolean> {
    let status: boolean = false;
    try {
      notifierLoading.value = true;

      const data = await notifiersApi.patchNotifier(uuid, patchNotifier);
      notifier.value = data;

      notifierError.value = null;
      status = true;
    } catch (err: unknown) {
      notifierError.value = getErrorMessage(err);
    } finally {
      notifierLoading.value = false;
    }
    return status;
  }

  async function fetchNotifierDelivery(
    uuid: string,
    forceLoad: boolean = false
  ) {
    if (
      !forceLoad &&
      notifierDelivery.value === uuid &&
      notifierDelivery.value != ""
    ) {
      return;
    }

    try {
      notifierDeliveryLoading.value = true;
      notifierDeliveryError.value = null;

      const data = await notifiersApi.getNotifierDelivery(uuid);
      notifierDelivery.value = data.delivery;
    } catch (err: unknown) {
      notifierDeliveryError.value = getErrorMessage(err);
    } finally {
      notifierDeliveryLoading.value = false;
    }
  }

  async function testNotifier(uuid: string): Promise<boolean> {
    let status: boolean = false;

    try {
      notifierTestLoading.value = true;
      await notifiersApi.testNotifier(uuid);
      status = true;
    } catch (err: unknown) {
      notifierError.value = getErrorMessage(err);
    } finally {
      notifierTestLoading.value = false;
    }
    return status;
  }

  async function deleteNotifier(uuid: string): Promise<boolean> {
    let status: boolean = false;
    try {
      notifierStateLoading.value = true;
      await notifiersApi.deleteNotifier(uuid);
      status = true;
    } catch (err: unknown) {
      console.error(err);
      status = false;
    } finally {
      notifierStateLoading.value = false;
    }

    return status;
  }

  return {
    notifier,
    notifierLoading,
    notifierError,
    notifierDelivery,
    notifierDeliveryLoading,
    notifierDeliveryError,

    getNotifier,
    getNotifierLoading,
    getNotifierError,
    getNotifierDelivery,
    getNotifierDeliveryLoading,
    getNotifierDeliveryError,
    getNotifierTestLoading,
    getNotifierStateLoading,

    fetchNotifier,
    addNotifier,
    patchNotifier,
    fetchNotifierDelivery,
    testNotifier,
    deleteNotifier,
  };
});
