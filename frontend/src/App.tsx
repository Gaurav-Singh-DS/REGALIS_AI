import { useEffect, useState } from 'react';
import type { User } from 'firebase/auth';
import { onAuthStateChanged } from 'firebase/auth';

import { InvestigationPage } from './pages/InvestigationPage';
import { Layout } from './components/layout/Layout';
import {
  auth,
  signInWithGoogle,
  logout,
} from './services/firebase';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [signingIn, setSigningIn] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(
      auth,
      (currentUser) => {
        setUser(currentUser);
        setLoading(false);
      },
      (authError) => {
        console.error('Firebase authentication error:', authError);
        setError('Unable to check your sign-in status. Please reload.');
        setLoading(false);
      }
    );

    return unsubscribe;
  }, []);

  async function handleGoogleSignIn() {
    setError('');
    setSigningIn(true);

    try {
      await signInWithGoogle();
    } catch (err) {
      console.error('Google sign-in failed:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Google sign-in failed. Please try again.'
      );
    } finally {
      setSigningIn(false);
    }
  }

  async function handleLogout() {
    try {
      await logout();
    } catch (err) {
      console.error('Sign-out failed:', err);
      setError('Unable to sign out. Please try again.');
    }
  }

  if (loading) {
    return (
      <div
        role="status"
        className="flex min-h-screen items-center justify-center gap-3 bg-banking-canvas text-sm text-banking-mute"
      >
        <svg className="h-4 w-4 animate-spin text-banking-primary" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.918l3-2.628z"></path>
        </svg>
        Checking your sign-in status...
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-banking-canvas px-4 py-10">
        <div className="w-full max-w-md overflow-hidden rounded-2xl border border-banking-border bg-white shadow-[0_18px_45px_rgba(13,37,61,0.12)]">
          <div className="flex items-center justify-between gap-3 bg-banking-navy px-6 py-5">
            <div className="flex items-center gap-3">
              <div
                aria-hidden="true"
                className="flex h-9 w-9 items-center justify-center rounded-xl bg-banking-primary text-sm font-bold text-white shadow-[0_6px_18px_rgba(83,58,253,0.35)]"
              >
                RA
              </div>
              <div className="leading-tight">
                <h1 className="text-lg font-semibold tracking-tight text-white">REGALIS AI</h1>
                <p className="text-[11px] uppercase tracking-[0.18em] text-slate-300">Risk Intelligence</p>
              </div>
            </div>
            <span className="rounded-full border border-white/15 bg-white/5 px-2.5 py-1 text-[10px] font-medium uppercase tracking-[0.18em] text-slate-200">
              Secure
            </span>
          </div>

          <div className="flex flex-col gap-6 px-6 py-7">
            <div className="space-y-2">
              <p className="text-sm font-medium text-banking-ink">Regulatory investigation workspace</p>
              <p className="text-sm leading-6 text-banking-mute">
                Sign in to access anomaly review, root cause analysis, and regulatory intelligence for the current report.
              </p>
            </div>

            <div className="grid grid-cols-3 gap-2 text-[11px] text-banking-mute">
              <div className="rounded-xl border border-banking-border bg-slate-50 px-3 py-2">
                <div className="font-semibold text-banking-ink">AI</div>
                <div>Review</div>
              </div>
              <div className="rounded-xl border border-banking-border bg-slate-50 px-3 py-2">
                <div className="font-semibold text-banking-ink">Risk</div>
                <div>Signals</div>
              </div>
              <div className="rounded-xl border border-banking-border bg-slate-50 px-3 py-2">
                <div className="font-semibold text-banking-ink">Audit</div>
                <div>Trail</div>
              </div>
            </div>

            <button
              onClick={handleGoogleSignIn}
              disabled={signingIn}
              aria-busy={signingIn}
              className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-banking-primary px-6 py-3 text-sm font-semibold text-white shadow-[0_10px_24px_rgba(83,58,253,0.28)] transition-all duration-200 hover:bg-banking-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true" className="h-4 w-4 fill-current">
                <path d="M21.6 12.23c0-.74-.06-1.45-.18-2.13H12v4.03h5.39a4.61 4.61 0 0 1-2 3.02v2.5h3.24c1.9-1.75 2.97-4.34 2.97-7.42Z" opacity=".3"/>
                <path d="M12 22c2.7 0 4.96-.9 6.61-2.43l-3.24-2.5c-.9.6-2.05.96-3.37.96-2.6 0-4.8-1.75-5.58-4.1H.9v2.58A10 10 0 0 0 12 22Zm0-8.77c1.3 0 2.46.45 3.38 1.33l2.54-2.52A6.8 6.8 0 0 0 12 6.5c-2.7 0-5.06 1.39-6.25 3.42l2.82 2.18A4.7 4.7 0 0 1 12 13.23Z"/>
                <path d="M12 13.23a4.7 4.7 0 0 1-4.64-3.8l-2.82-2.18A7.3 7.3 0 0 0 12 6.5a7.18 7.18 0 0 1 4.93 1.8l2.3-2.3A9.9 9.9 0 0 0 12 2a10 10 0 0 0-9.1 5.52l2.85 2.2A6.09 6.09 0 0 1 12 13.23Z" opacity=".3"/>
              </svg>
              {signingIn ? 'Signing in...' : 'Sign in with Google'}
            </button>

            {error && (
              <p
                role="alert"
                className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-anomaly-red"
              >
                {error}
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="border-b border-banking-border bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-end gap-3 px-4 py-2 text-sm sm:px-6">
          <span className="truncate text-banking-mute">{user.email}</span>
          <button
            onClick={handleLogout}
            className="min-h-9 shrink-0 rounded-md border border-banking-border bg-white px-3 py-1.5 text-sm font-medium text-banking-ink transition-colors duration-200 hover:bg-slate-50"
          >
            Sign out
          </button>
        </div>
      </div>

      {error && (
        <div className="mx-auto max-w-7xl px-4 pt-4 sm:px-6">
          <p
            role="alert"
            className="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-sm text-anomaly-red"
          >
            {error}
          </p>
        </div>
      )}

      <Layout>
        <InvestigationPage reportId="rep_credit_risk_2026_09" />
      </Layout>
    </div>
  );
}

export default App;
