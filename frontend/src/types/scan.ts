export enum ScanStatus {
  pending = 0,
  running = 1,
  completed = 2,
  failed = 3,
}

export enum ScanType {
  simple = 0,
  complex = 1,
}

export interface Scan {
  id: number;
  type: ScanType;
  url: string;
  status: ScanStatus;
  created_at: string;
  progress: number;
  current_step: string;
  data: string;
  creator_id: number;
  score: number | null;
}

export const getScanTypeText = (type: ScanType): string => {
  switch (type) {
    case ScanType.simple:
      return "Simple";
    case ScanType.complex:
      return "Complex";
    default:
      return "Unknown";
  }
};

export const getScanStatusText = (status: ScanStatus): string => {
  switch (status) {
    case ScanStatus.pending:
      return "Pending";
    case ScanStatus.running:
      return "Running";
    case ScanStatus.completed:
      return "Completed";
    case ScanStatus.failed:
      return "Failed";
    default:
      return "Unknown";
  }
};

export const getScanStatusClass = (status: ScanStatus): string => {
  switch (status) {
    case ScanStatus.pending:
      return "badge-warning";
    case ScanStatus.running:
      return "badge-info";
    case ScanStatus.completed:
      return "badge-success";
    case ScanStatus.failed:
      return "badge-error";
    default:
      return "badge-ghost";
  }
};

export interface Result {
  id: number;
  title: string;
  severity: number;
  category: number;
  description: string;
  short_description: string;
  recommendation: string;
  score: number;
  scan_id: number;
}

export const getSeverityLabel = (severity: number): string => {
  switch (severity) {
    case 0:
      return "Debug";
    case 1:
      return "Info";
    case 2:
      return "Warning";
    case 3:
      return "Error";
    case 4:
      return "Critical";
    default:
      return "Unknown";
  }
};

export const getSeverityClass = (severity: number): string => {
  switch (severity) {
    case 0:
      return "badge-ghost"; // Debug
    case 1:
      return "badge-info"; // Info
    case 2:
      return "badge-warning"; // Warning
    case 3:
      return "badge-error"; // Error
    case 4:
      return "badge-neutral"; // Critical
    default:
      return "badge-ghost";
  }
};

export const getCategoryLabel = (category: number): string => {
  switch (category) {
    case 0:
      return "Unknown";
    default:
      return "Unknown";
  }
};
