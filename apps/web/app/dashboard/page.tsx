import { Topbar } from '@/components/topbar';
import { StatCard } from '@/components/stat-card';
import { Shield, Users, Scale, AlertTriangle } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div>
      <Topbar title="Sentinel Intelligence Vault" subtitle="Secure Personal Legal Intelligence & Dispute Record Management System" />
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total Persons / کل افراد" value="0000" icon={<Users className="h-5 w-5" />} />
        <StatCard title="Active Cases / فعال مقدمات" value="0000" icon={<Scale className="h-5 w-5" />} />
        <StatCard title="High Risk Persons / زیادہ خطرہ" value="0000" icon={<AlertTriangle className="h-5 w-5" />} />
        <StatCard title="Vault Security / والٹ سیکیورٹی" value="Protected" icon={<Shield className="h-5 w-5" />} />
      </section>
      <section className="mt-6 grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow">
          <h3 className="mb-3 text-lg font-semibold">Operational Summary / عملی خلاصہ</h3>
          <p className="text-sm leading-7 text-muted">
            Enterprise-grade dashboard prepared for legal record organization, threat review, financial exposure monitoring,
            incident logging, and confidential documentation management.
          </p>
        </div>
        <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow">
          <h3 className="mb-3 text-lg font-semibold">Alerts / الرٹس</h3>
          <ul className="space-y-3 text-sm text-muted">
            <li>Risk increase monitoring active.</li>
            <li>Court date reminders ready for integration.</li>
            <li>Manual encrypted backup workflow prepared.</li>
          </ul>
        </div>
      </section>
    </div>
  );
}
