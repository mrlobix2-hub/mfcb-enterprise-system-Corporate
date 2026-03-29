import { Topbar } from '@/components/topbar';

export default function ReportsPage() {
  return (
    <div>
      <Topbar title="Reports / رپورٹس" subtitle="Generate professional confidential legal documentation reports." />
      <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow text-muted">
        PDF generator integration point prepared for confidential, watermarked report rendering.
      </div>
    </div>
  );
}
