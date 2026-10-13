import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import { MetricCard } from '../components/dashboard/MetricCard';
import { RcaPanel } from '../components/investigation/RcaPanel';

interface ReportMetric {
  metric_id: string;
  metric_name: string;
  previous_value: number;
  current_value: number;
  delta_pct: number;
  is_anomaly: boolean;
}

interface Anomaly {
  metric_id: string;
  metric_name: string;
  delta_pct: number;
  severity: 'CRITICAL' | 'WARNING' | 'INFO';
  status: string;
}

interface AgentFinding {
  agent: string;
  finding: string;
  status: string;
  sources?: string[];
}

interface InvestigationResult {
  investigationId: string;
  detected_anomaly: Anomaly;
  root_cause: string;
  evidence: AgentFinding[];
  confidence: string;
  status: string;
}

type MetricsStatus = 'loading' | 'ready' | 'error';

export const InvestigationPage: React.FC<{ reportId: string }> = ({ reportId }) => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [metrics, setMetrics] = useState<ReportMetric[]>([]);
  const [metricsStatus, setMetricsStatus] = useState<MetricsStatus>('loading');
  const [investigationFailed, setInvestigationFailed] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const loadMetrics = async () => {
      setMetricsStatus('loading');

      try {
        const data = await api.getMetrics<ReportMetric[]>(reportId);

        if (!cancelled) {
          setMetrics(data);
          setMetricsStatus('ready');
        }
      } catch (err) {
        console.error('Error loading metrics:', err);

        if (!cancelled) {
          setMetricsStatus('error');
        }
      }
    };

    void loadMetrics();

    return () => {
      cancelled = true;
    };
  }, [reportId]);

  const handleInvestigate = async () => {
    setLoading(true);
    setInvestigationFailed(false);

    try {
      const res = await api.startInvestigation<InvestigationResult>(reportId);
      setResult(res);
    } catch (e) {
      console.error('Investigation failed', e);
      setInvestigationFailed(true);
    } finally {
      setLoading(false);
    }
  };

  const anomalyCount = metrics.filter((m) => m.is_anomaly).length;

  return (
    <div className="mx-auto max-w-7xl font-sans" >
      <section
        aria-labelledby="report-title"
        className="mb-8 overflow-hidden rounded-[28px] border border-banking-border bg-white p-5 shadow-[0_18px_45px_rgba(13,37,61,0.06)] sm:p-6"
      >
        <div className="mb-5 flex items-center justify-between gap-3 border-b border-banking-border pb-4">
          <div className="flex items-center gap-3">
            <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-violet-50 text-lg text-banking-primary">
              📊
            </span>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-banking-mute">Portfolio review</p>
              <h1 id="report-title" className="text-2xl font-semibold tracking-tight text-banking-ink sm:text-3xl">
                Report Investigation
              </h1>
            </div>
          </div>

          <span className="inline-flex rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-slate-600 ring-1 ring-inset ring-slate-200">
            Draft
          </span>
        </div>

        <div className="flex flex-col gap-5 md:flex-row md:items-end md:justify-between">
          <dl className="grid grid-cols-1 gap-x-8 gap-y-3 text-sm sm:grid-cols-3">
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-banking-mute">Report ID</dt>
              <dd className="mt-1 break-all font-semibold text-banking-ink">{reportId}</dd>
            </div>
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-banking-mute">Period</dt>
              <dd className="mt-1 font-semibold text-banking-ink">September 2026</dd>
            </div>
            <div>
              <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-banking-mute">Status</dt>
              <dd className="mt-1 font-semibold text-banking-ink">Pending Review</dd>
            </div>
          </dl>

          <button
            onClick={handleInvestigate}
            disabled={loading}
            aria-busy={loading}
            className="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-banking-primary px-5 py-2.5 text-sm font-semibold text-white shadow-[0_12px_24px_rgba(83,58,253,0.22)] transition-all duration-200 hover:bg-banking-primary-dark focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-banking-primary disabled:cursor-not-allowed disabled:bg-slate-300 disabled:text-slate-500"
          >
            {loading ? (
              <>
                <svg className="h-4 w-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.918l3-2.628z"></path>
                </svg>
                Executing Analysis...
              </>
            ) : (
              'Run Root Cause Analysis'
            )}
          </button>
        </div>
      </section>

      <section aria-labelledby="metrics-heading" className="mb-10">
        <div className="mb-4 flex flex-wrap items-baseline justify-between gap-2">
          <h2 id="metrics-heading" className="text-lg font-semibold text-banking-ink">
            Report metrics
          </h2>
          {metricsStatus === 'ready' && metrics.length > 0 && (
            <p className="text-sm text-banking-mute">
              {metrics.length} {metrics.length === 1 ? 'metric' : 'metrics'}
              {anomalyCount > 0 && (
                <>
                  {' '}&middot;{' '}
                  <span className="font-semibold text-warning-amber">
                    {anomalyCount} {anomalyCount === 1 ? 'anomaly' : 'anomalies'}
                  </span>
                </>
              )}
            </p>
          )}
        </div>

        {metricsStatus === 'loading' && (
          <div role="status" aria-live="polite" className="grid grid-cols-1 gap-5 md:grid-cols-3">
            <span className="sr-only">Loading report metrics</span>
            {[0, 1, 2].map((i) => (
              <div key={i} aria-hidden="true" className="h-40 animate-pulse rounded-2xl border border-banking-border bg-white p-5 shadow-[0_10px_24px_rgba(13,37,61,0.04)]">
                <div className="h-3 w-1/2 rounded bg-slate-200"></div>
                <div className="mt-6 h-8 w-1/3 rounded bg-slate-200"></div>
                <div className="mt-8 h-3 w-full rounded bg-slate-100"></div>
              </div>
            ))}
          </div>
        )}

        {metricsStatus === 'error' && (
          <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-anomaly-red">
            <p className="font-semibold">Metrics could not be loaded</p>
            <p className="mt-1 text-red-800">
              Reload the page to try again. If the problem continues, contact your administrator.
            </p>
          </div>
        )}

        {metricsStatus === 'ready' && metrics.length === 0 && (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-10 text-center">
            <p className="text-sm font-semibold text-banking-ink">No metrics available</p>
            <p className="mt-1 text-sm text-banking-mute">This report has no metrics to display yet.</p>
          </div>
        )}

        {metricsStatus === 'ready' && metrics.length > 0 && (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {metrics.map((m) => (
              <MetricCard key={m.metric_id} metric={m} />
            ))}
          </div>
        )}
      </section>

      <section aria-labelledby="rca-heading" aria-live="polite" className="mb-4">
        {(loading || investigationFailed || result) && (
          <h2 id="rca-heading" className="mb-4 text-lg font-semibold text-banking-ink">
            Root cause analysis
          </h2>
        )}

        {loading && (
          <div
            role="status"
            className="rounded-2xl border border-banking-border bg-white p-6 text-sm text-banking-mute shadow-[0_10px_24px_rgba(13,37,61,0.04)]"
          >
            <div className="flex items-center gap-3">
              <svg className="h-4 w-4 animate-spin text-banking-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.918l3-2.628z"></path>
              </svg>
              Executing root cause analysis for this report...
            </div>
          </div>
        )}

        {investigationFailed && !result && (
          <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-anomaly-red">
            <p className="font-semibold">The analysis could not be completed</p>
            <p className="mt-1 text-red-800">
              Please try again. If the issue persists, contact the reporting team.
            </p>
          </div>
        )}

        {result && <RcaPanel result={result} />}
      </section>
    </div>
  );
};
