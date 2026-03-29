const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api';

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    credentials: 'include',
    cache: 'no-store',
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'API request failed');
  }

  return response.json();
}
