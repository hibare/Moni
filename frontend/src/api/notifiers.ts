import {
  HistoryType,
  JobType,
  NotifierAddEditType,
  NotifierDeliveryType,
  NotifierType,
} from "../types";
import axios from "../utils/axios";

async function getNotifiers(): Promise<Array<NotifierType>> {
  const { data } = await axios.get<Array<NotifierType>>("/api/v1/notifiers/");
  return data;
}

async function getNotifier(uuid: string): Promise<NotifierType> {
  const { data } = await axios.get<NotifierType>(`/api/v1/notifiers/${uuid}/`);
  return data;
}

async function addNotifier(
  notifier: NotifierAddEditType
): Promise<NotifierType> {
  const { data } = await axios.post<NotifierType>(
    `/api/v1/notifiers/`,
    notifier
  );
  return data;
}

async function patchNotifier(
  uuid: string,
  notifier: NotifierAddEditType
): Promise<NotifierType> {
  const { data } = await axios.patch<NotifierType>(
    `/api/v1/notifiers/${uuid}/`,
    notifier
  );
  return data;
}

async function getNotifierJobs(uuid: string): Promise<Array<JobType>> {
  const { data } = await axios.get<Array<JobType>>(
    `/api/v1/notifiers/${uuid}/jobs/`
  );
  return data;
}

async function getNotifierDelivery(
  uuid: string
): Promise<NotifierDeliveryType> {
  const { data } = await axios.get<NotifierDeliveryType>(
    `/api/v1/notifiers/${uuid}/delivery/`
  );
  return data;
}

async function getNotifierHistory(uuid: string): Promise<Array<HistoryType>> {
  const { data } = await axios.get<Array<HistoryType>>(
    `/api/v1/notifiers/${uuid}/history/`
  );
  return data;
}

async function deleteNotifierHistory(uuid: string): Promise<void> {
  await axios.delete(`/api/v1/notifiers/${uuid}/history/`);
}

async function testNotifier(uuid: string) {
  await axios.post(`/api/v1/notifiers/${uuid}/test/`);
}

async function deleteNotifier(uuid: string) {
  await axios.delete(`/api/v1/notifiers/${uuid}/`);
}

async function testBareNotifier(notifier: NotifierAddEditType): Promise<void> {
  await axios.post("/api/v1/notifiers/test/", notifier);
}

const notifiersApi = {
  getNotifiers,
  getNotifier,
  addNotifier,
  patchNotifier,
  getNotifierDelivery,
  getNotifierJobs,
  getNotifierHistory,
  deleteNotifierHistory,
  testNotifier,
  deleteNotifier,
  testBareNotifier,
};

export default notifiersApi;
