'use client';

import { useState } from 'react';

export default function LoginPage() {
  const [username, setUsername] = useState('admin_siv');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api'}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, password }),
    });
    const payload = await response.json();
    setMessage(payload.message || 'Done');
  }

  return (
    <div className="mx-auto max-w-md rounded-3xl border border-border bg-panel p-8 shadow-glow">
      <h1 className="mb-2 text-2xl font-semibold">Admin Login / ایڈمن لاگ ان</h1>
      <p className="mb-6 text-sm text-muted">Default admin must change password on first login.</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input value={username} onChange={(e) => setUsername(e.target.value)} className="w-full rounded-xl border bg-background px-4 py-3" placeholder="Username" />
        <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" className="w-full rounded-xl border bg-background px-4 py-3" placeholder="Password" />
        <button className="w-full rounded-xl bg-slate-200 px-4 py-3 font-medium text-slate-900">Sign in</button>
      </form>
      {message ? <p className="mt-4 text-sm text-accent">{message}</p> : null}
    </div>
  );
}
