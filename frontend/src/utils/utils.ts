import { copyToClipboard, Notify } from "quasar";
import { NotifyPosition, NotifyStatus } from "../constants";
import { NotificationType } from "../types";

export function showNotify(notification: NotificationType) {
  Notify.create({
    type: notification.status,
    color: notification.status,
    position: NotifyPosition.DefaultNotifyPosition,
    message: notification.message,
    progress: true,
    timeout: 2500,
  });
}

export function getErrorMessage(err: unknown): string {
  if (typeof err === "string") {
    return err.toUpperCase();
  } else if (err instanceof Error) {
    return err.message;
  }
  return "Unknown Error";
}

export function copy2Clipboard(val: string) {
  var notification = {} as NotificationType;
  copyToClipboard(val)
    .then(() => {
      notification.status = NotifyStatus.Success;
      notification.message = "Copied to clipboard";
    })
    .catch(() => {
      notification.status = NotifyStatus.Warning;
      notification.message = "Failed to copy";
    })
    .finally(() => {
      if (notification) {
        showNotify(notification);
      }
    });
}

export function prettyDate(d: Date | string): string {
  // Convert zulu date string to pretty date string (local)
  let dObj;

  if (Object.prototype.toString.call(d) !== "[object Date]") dObj = new Date(d);
  else dObj = d as Date;

  const today = new Date();
  const yesterday = new Date(today);

  yesterday.setDate(yesterday.getDate() - 1);

  if (today.toDateString() === dObj.toDateString()) {
    // Today
    return (
      "Today " +
      dObj.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      })
    );
  } else if (yesterday.toDateString() === dObj.toDateString()) {
    // Yesterday
    return (
      "Yesterday " +
      dObj.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      })
    );
  } else {
    return dObj.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    });
  }
}
