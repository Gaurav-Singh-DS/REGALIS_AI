import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface RcaPanelProps {
  result: {
    root_cause: string;
    confidence: string;
    status: string;
    evidence: {
      agent: string;
      finding: string;
    }[];
  };
}

export const RcaPanel: React.FC<RcaPanelProps> = ({ result }) => {
  const [expandedEvidence, setExpandedEvidence] = useState<string | null>(null);

  const toggleEvidence = (agent: string) => {
    setExpandedEvidence((current) => (current === agent ? null : agent));
  };

  return (
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-[minmax(0,2fr)_minmax(260px,1fr)]">
      <div className="space-y-6">
        <div className="relative overflow-hidden rounded-2xl border border-banking-border bg-white p-6 shadow-[0_12px_30px_rgba(13,37,61,0.06)] sm:p-8">
          <div className="absolute inset-y-0 left-0 w-1 bg-banking-primary"></div>

          <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="space-y-2">
              <h2 className="flex items-center gap-3 text-xl font-semibold tracking-tight text-banking-ink">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-violet-50 text-lg text-banking-primary">🎯</span>
                Root Cause Analysis
              </h2>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-banking-mute">
                Institutional Intelligence Report
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <div className="flex items-center gap-2 rounded-full border border-banking-border bg-slate-50 px-3 py-1.5">
                <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-banking-mute">Confidence</span>
                <span className="text-xs font-bold text-banking-ink">{result.confidence}</span>
              </div>
              <div className="flex items-center gap-2 rounded-full border border-red-100 bg-red-50 px-3 py-1.5">
                <span className="text-[10px] font-semibold uppercase tracking-[0.18em] text-anomaly-red">Status</span>
                <span className="text-xs font-bold text-anomaly-red">{result.status}</span>
              </div>
            </div>
          </div>

          <div
            className="prose prose-slate max-w-none text-banking-ink
            prose-headings:mt-6 prose-headings:mb-3 prose-headings:font-semibold prose-headings:tracking-tight prose-headings:text-banking-ink
            prose-p:mt-3 prose-p:leading-7 prose-p:text-slate-600 prose-p:font-normal
            prose-strong:text-banking-ink prose-strong:font-semibold
            prose-li:leading-7 prose-li:text-slate-600
            prose-code:bg-slate-100 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded-md prose-code:text-banking-ink
            prose-pre:bg-slate-900 prose-pre:text-slate-100 prose-pre:p-4 prose-pre:rounded-xl prose-pre:border prose-pre:border-slate-700"
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.root_cause}</ReactMarkdown>
          </div>
        </div>
      </div>

      <aside className="space-y-6">
        <div className="rounded-2xl border border-banking-border bg-white p-5 shadow-[0_10px_24px_rgba(13,37,61,0.05)]">
          <h2 className="mb-5 flex items-center gap-2 text-lg font-semibold text-banking-ink">
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-violet-50 text-base text-banking-primary">🔍</span>
            Evidence Trail
          </h2>

          <div className="space-y-3">
            {result.evidence.map((e, i) => (
              <button
                key={`${e.agent}-${i}`}
                type="button"
                onClick={() => toggleEvidence(e.agent)}
                className={`w-full rounded-xl border p-4 text-left transition-all duration-200 ${
                  expandedEvidence === e.agent
                    ? 'border-banking-primary bg-violet-50/50 shadow-[0_8px_18px_rgba(83,58,253,0.08)]'
                    : 'border-banking-border bg-white hover:border-slate-400 hover:bg-slate-50'
                }`}
              >
                <div className="mb-2 flex items-center justify-between gap-3">
                  <p className="text-[10px] font-semibold uppercase tracking-[0.18em] text-banking-primary">{e.agent}</p>
                  <span className="text-[10px] text-banking-mute">{expandedEvidence === e.agent ? '▲' : '▼'}</span>
                </div>
                <p
                  className={`text-sm leading-6 transition-all duration-200 ${
                    expandedEvidence === e.agent ? 'text-banking-ink' : 'line-clamp-2 text-banking-mute italic'
                  }`}
                >
                  “{e.finding}”
                </p>
              </button>
            ))}
          </div>
        </div>
      </aside>
    </div>
  );
};
