import { ReactNode } from 'react';

export function StatCard({ title, value, icon }: { title: string; value: string | number; icon?: ReactNode }) {
  return (
    <div className="rounded-2xl border border-border bg-panel p-5 shadow-glow">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-sm text-muted">{title}</p>
        <div className="text-accent">{icon}</div>
      </div>
      <p className="text-3xl font-semibold tracking-tight">{value}</p>
    </div>
  );
}
