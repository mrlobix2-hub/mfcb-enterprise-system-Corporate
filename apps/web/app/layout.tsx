import './globals.css';
import { Sidebar } from '@/components/sidebar';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sentinel Intelligence Vault',
  description: 'Secure Personal Legal Intelligence & Dispute Record Management System',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen md:flex">
          <Sidebar />
          <main className="flex-1 p-6 md:p-10">{children}</main>
        </div>
      </body>
    </html>
  );
}
