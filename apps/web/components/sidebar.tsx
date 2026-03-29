'use client';

import Link from 'next/link';
import { LayoutDashboard, Shield, Users, Scale, AlertTriangle, FileText, Settings } from 'lucide-react';

const nav = [
  { href: '/dashboard', label: 'Dashboard / ڈیش بورڈ', icon: LayoutDashboard },
  { href: '/persons', label: 'Persons / افراد', icon: Users },
  { href: '/cases', label: 'Cases / مقدمات', icon: Scale },
  { href: '/incidents', label: 'Incidents / واقعات', icon: AlertTriangle },
  { href: '/reports', label: 'Reports / رپورٹس', icon: FileText },
  { href: '/settings', label: 'Settings / ترتیبات', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden md:flex md:w-72 flex-col border-r border-border bg-panel/60 p-5">
      <div className="mb-8 rounded-2xl border border-border bg-background p-4 shadow-glow">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-slate-200/10 p-3"><Shield className="h-6 w-6" /></div>
          <div>
            <p className="text-sm text-accent">Sentinel Intelligence Vault</p>
            <h1 className="text-lg font-semibold">SIV Control</h1>
          </div>
        </div>
      </div>
      <nav className="space-y-2">
        {nav.map((item) => {
          const Icon = item.icon;
          return (
            <Link key={item.href} href={item.href} className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-200 transition hover:bg-slate-200/5">
              <Icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
