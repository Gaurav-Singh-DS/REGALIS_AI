import React from 'react';

interface MetricCardProps {
  metric: {
    metric_id: string;
    metric_name: string;
    previous_value: number;
    current_value: number;
    delta_pct: number;
    is_anomaly: boolean;
  };
}

export const MetricCard: React.FC<MetricCardProps> = ({ metric }) => {
  const isAnomaly = metric.is_anomaly;
  const isUp = metric.delta_pct > 0;
  const formatValue = (value: number) => new Intl.NumberFormat('en-US').format(value);

  return (
    <article
      aria-label={metric.metric_name}
      className={[
        'relative flex flex-col justify-between rounded-2xl border bg-white p-5 shadow-[0_10px_24px_rgba(13,37,61,0.06)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_28px_rgba(13,37,61,0.08)]',
        isAnomaly ? 'border-l-4 border-l-warning-amber border-banking-border' : 'border-banking-border',
      ].join(' ')}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.16em] text-banking-mute">Key metric</p>
          <h3 className="mt-2 text-base font-semibold leading-snug text-banking-ink">{metric.metric_name}</h3>
        </div>
        {isAnomaly && (
          <span className="inline-flex shrink-0 items-center gap-1 rounded-full bg-amber-50 px-2 py-1 text-[11px] font-semibold text-warning-amber ring-1 ring-inset ring-amber-200">
            <svg aria-hidden="true" viewBox="0 0 20 20" fill="currentColor" className="h-3.5 w-3.5">
              <path fillRule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
            </svg>
            Anomaly
          </span>
        )}
      </div>

      <div className="mt-5 flex flex-wrap items-end gap-x-3 gap-y-2">
        <p className="text-3xl font-semibold tabular-nums tracking-tight text-banking-ink">
          {formatValue(metric.current_value)}
        </p>
        <span
          className={`inline-flex items-center gap-1 rounded-full px-2 py-1 text-[11px] font-semibold tabular-nums ${
            isUp ? 'bg-red-50 text-anomaly-red' : 'bg-green-50 text-healthy-green'
          }`}
        >
          <span aria-hidden="true">{isUp ? '▲' : '▼'}</span>
          <span className="sr-only">{isUp ? 'Increase of' : 'Decrease of'}</span>
          {Math.abs(metric.delta_pct)}%
        </span>
      </div>

      <dl className="mt-5 flex items-center justify-between border-t border-banking-border pt-3 text-xs">
        <dt className="text-banking-mute">Previous period</dt>
        <dd className="font-semibold tabular-nums text-banking-ink">{formatValue(metric.previous_value)}</dd>
      </dl>
    </article>
  );
};
