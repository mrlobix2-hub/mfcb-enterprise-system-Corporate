import { Topbar } from '@/components/topbar';

export default function SettingsPage() {
  return (
    <div>
      <Topbar title="Settings / ترتیبات" subtitle="Manage credentials, language, theme, and security preferences." />
      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow">
          <h3 className="mb-3 text-lg font-semibold">Security / سیکیورٹی</h3>
          <p className="text-sm text-muted">Password change, recovery email, and security question flows are wired through the API scaffold.</p>
        </div>
        <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow">
          <h3 className="mb-3 text-lg font-semibold">Language / زبان</h3>
          <p className="text-sm text-muted">UI labels are prepared in bilingual English + Urdu style.</p>
        </div>
      </div>
    </div>
  );
}
