export enum ScanStatus {
  pending = 0,
  running = 1,
  completed = 2,
  failed = 3,
}

export enum ScanType {
  simple = 0,
  complexe = 1,
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
  result: number;
}

export const getScanTypeText = (type: ScanType): string => {
  switch (type) {
    case ScanType.simple:
      return "Simple";
    case ScanType.complexe:
      return "Complexe";
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
