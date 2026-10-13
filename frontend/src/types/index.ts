export interface ReportMetric {
    metric_id: string;
    metric_name: string;
    previous_value: number;
    current_value: number;
    delta_pct: number;
    is_anomaly: boolean;
  }

export interface Report {
    id: string;
    name: string;
    period: string;
    status: string;
  }

export interface Anomaly {
    metric_id: string;
    metric_name: string;
    delta_pct: number;
    severity: 'CRITICAL' | 'WARNING' | 'INFO';
    status: string;
  }

export interface AgentFinding {
    agent: string;
    finding: string;
    status: string;
    sources?: string[];
  }

export interface InvestigationResult {
    investigationId: string;
    detected_anomaly: Anomaly;
    root_cause: string;
    evidence: AgentFinding[];
    confidence: string;
    status: string;
  }
