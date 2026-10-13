import { auth } from './firebase';

const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ||
  'https://regalis-ai-backend-526000967059.us-central1.run.app'
).replace(/\/$/, '');

async function request<T = unknown>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const user = auth.currentUser;
  const token = user ? await user.getIdToken() : null;

  const headers = new Headers(options.headers ?? {});
  if (token) {
    headers.set('Authorization', 'Bearer ' + token);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const details = await response.text();
    throw new Error(`API request failed (${response.status}): ${details}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  async getReport<T = unknown>(id: string) {
    return request<T>(`/api/reports/${encodeURIComponent(id)}`);
  },

  async getMetrics<T = unknown>(id: string) {
    return request<T>(`/api/reports/${encodeURIComponent(id)}/metrics`);
  },

  async startInvestigation<T = unknown>(id: string) {
    return request<T>(`/api/investigations/${encodeURIComponent(id)}`, {
      method: 'POST',
    });
  },
};
