export type JWTLoginResponseType = {
  refresh: string;
  access: string;
  firstname: string;
  lastname: string;
  fullname: string;
  email: string;
  is_staff: boolean;
  is_superuser: boolean;
};

export type NotificationType = {
  status: string;
  message: string;
};

export type JobType = {
  uuid: string;
  notifiers: Array<string>;
  created: string;
  updated: string;
  url: string;
  title: string;
  state: boolean;
  headers: Record<string, any>;
  verify_ssl: boolean;
  interval: number;
  success_status: Array<number>;
  check_redirect: boolean;
  healthy: boolean;
  favicon_url: string | null;
  failure_threshold: number;
};

export type JobUptimeType = {
  uptime: string;
};

export type JobResponseTimeType = {
  response: string;
};

export type HistoryType = {
  id: number;
  timestamp: string;
  status_code: number;
  success: boolean;
  response_time: number;
  error: string | null;
  uuid: string;
};

export type NotifierType = {
  uuid: string;
  created: string;
  updated: string;
  url: string;
  type: string;
  title: string;
  description: string;
};

export type JobAddEditType = {
  title: string;
  url: string;
  interval: number;
  state: boolean;
  verify_ssl: boolean;
  check_redirect: boolean;
  headers: Record<string, any>;
  notifiers: Array<string>;
  success_status: Array<number>;
  failure_threshold: number;
};

export type HeaderType = {
  key: string;
  value: string | number;
};

export type NotifierDeliveryType = {
  delivery: string;
};

export type NotifierAddEditType = {
  title: string;
  description: string;
  url: string;
  type: string;
  valid?: boolean;
};

export type AccountType = {
  first_name: string;
  last_name: string;
  email: string;
};

export type PasswordType = {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
};

export type APITokenType = {
  token: string;
};
