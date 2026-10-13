import React from 'react';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-banking-canvas font-sans text-banking-ink selection:bg-banking-primary/20">
      <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-banking-navy shadow-[0_4px_20px_rgba(8,29,53,0.24)] backdrop-blur-sm">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <div
              aria-hidden="true"
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-banking-primary text-sm font-bold text-white shadow-[0_8px_20px_rgba(83,58,253,0.35)]"
            >
              RA
            </div>
            <div className="min-w-0 leading-tight">
              <p className="truncate text-sm font-semibold tracking-tight text-white">REGALIS AI</p>
              <p className="hidden truncate text-[11px] uppercase tracking-[0.18em] text-slate-300 sm:block">
                Regulatory Intelligence Platform
              </p>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-3 sm:gap-5">
            <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-2.5 py-1.5 text-[11px]">
              <span className="relative flex h-2 w-2" aria-hidden="true">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-70"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400"></span>
              </span>
              <span className="text-slate-300">
                <span className="hidden sm:inline">AI engine:</span>
                <span className="ml-1 font-semibold text-white">Gemini</span>
              </span>
            </div>

            <div className="flex items-center gap-3 border-l border-white/12 pl-3 sm:pl-5">
              <div className="hidden text-right sm:block">
                <p className="text-sm font-semibold leading-none text-white">Gaurav</p>
                <p className="mt-1 text-[11px] uppercase tracking-[0.14em] text-slate-300">Chief Risk Officer</p>
              </div>
              <div
                aria-hidden="true"
                className="flex h-8 w-8 items-center justify-center rounded-full bg-white/10 text-xs font-semibold text-white ring-1 ring-white/15"
              >
                G
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:py-10">
        {children}
      </main>
    </div>
  );
};
