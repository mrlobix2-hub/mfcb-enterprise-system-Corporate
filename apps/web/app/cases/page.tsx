import { Topbar } from '@/components/topbar';

export default function CasesPage() {
  return (
    <div>
      <Topbar title="Legal Case Management / قانونی مقدمات" subtitle="Track FIRs, police matters, lawyers, courts, and hearings." />
      <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow text-muted">
        Case grid, hearing calendar, and outcome tracker hooks are prepared in the Prisma schema and API scaffold.
      </div>
    </div>
  );
}
