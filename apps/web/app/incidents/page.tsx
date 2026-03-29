import { Topbar } from '@/components/topbar';

export default function IncidentsPage() {
  return (
    <div>
      <Topbar title="Incident Reports / واقعہ رپورٹس" subtitle="Log chronology, location, description, impact, and evidence." />
      <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow text-muted">
        Incident reporting forms should submit to `/api/incidents` once route handlers are added.
      </div>
    </div>
  );
}
