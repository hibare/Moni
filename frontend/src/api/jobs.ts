import axios from "../utils/axios";
import {
  JobAddEditType,
  HistoryType,
  JobResponseTimeType,
  JobType,
  JobUptimeType,
  NotifierType,
} from "../types";

async function getJobs(): Promise<Array<JobType>> {
  const { data } = await axios.get<Array<JobType>>("/api/v1/jobs/");
  return data;
}

async function getJob(uuid: string): Promise<JobType> {
  const { data } = await axios.get<JobType>(`/api/v1/jobs/${uuid}/`);
  return data;
}

async function addJob(job: JobAddEditType): Promise<JobType> {
  const { data } = await axios.post<JobType>(`/api/v1/jobs/`, job);
  return data;
}

async function patchJob(uuid: string, job: JobAddEditType): Promise<JobType> {
  const { data } = await axios.patch<JobType>(`/api/v1/jobs/${uuid}/`, job);
  return data;
}

async function getJobUptime(uuid: string): Promise<JobUptimeType> {
  const { data } = await axios.get<JobUptimeType>(
    `/api/v1/jobs/${uuid}/uptime/`
  );
  return data;
}

async function getJobResponseTime(uuid: string): Promise<JobResponseTimeType> {
  const { data } = await axios.get<JobResponseTimeType>(
    `/api/v1/jobs/${uuid}/response/`
  );
  return data;
}

async function getJobNotifiers(uuid: string): Promise<Array<NotifierType>> {
  const { data } = await axios.get<Array<NotifierType>>(
    `/api/v1/jobs/${uuid}/notifiers/`
  );
  return data;
}

async function getJobHistory(uuid: string): Promise<Array<HistoryType>> {
  const { data } = await axios.get<Array<HistoryType>>(
    `/api/v1/jobs/${uuid}/history/`
  );
  return data;
}

async function pauseJob(uuid: string) {
  await axios.post(`/api/v1/jobs/${uuid}/pause/`);
}

async function resumeJob(uuid: string) {
  await axios.post(`/api/v1/jobs/${uuid}/resume/`);
}

async function deleteJob(uuid: string) {
  await axios.delete(`/api/v1/jobs/${uuid}/`);
}

async function deleteJobHistory(uuid: string) {
  await axios.delete(`/api/v1/jobs/${uuid}/history/`);
}

const jobsApi = {
  getJobs,
  getJob,
  addJob,
  patchJob,
  getJobUptime,
  getJobResponseTime,
  getJobNotifiers,
  getJobHistory,
  pauseJob,
  resumeJob,
  deleteJob,
  deleteJobHistory,
};

export default jobsApi;
