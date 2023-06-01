import { QNotifyCreateOptions } from "quasar";

export const AppName: string = "Moni";

export const NotifyStatus: Record<string, string> = {
  Success: "positive",
  Warning: "warning",
  Error: "negative",
  Info: "info",
};

export const NotifyPosition: Record<string, QNotifyCreateOptions["position"]> =
  {
    TopLeft: "top-left",
    TopRight: "top-right",
    BottomLeft: "bottom-left",
    BottomRight: "bottom-right",
    Top: "top",
    Bottom: "bottom",
    Left: "left",
    Right: "right",
    Center: "center",
  };

export const DefaultNotifyPosition: QNotifyCreateOptions["position"] =
  NotifyPosition.TopRight;

export const StatusCodes: Array<Number> = [
  200, 201, 202, 203, 204, 100, 101, 102, 205, 206, 207, 208, 226, 300, 301,
  302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408,
  409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 421, 422, 423, 424, 426,
  428, 429, 431, 444, 451, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508,
  510, 511, 599,
];
