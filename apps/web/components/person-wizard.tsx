'use client';

import { useMemo, useState } from 'react';

const steps = [
  'Basic Info / بنیادی معلومات',
  'Risk Data / خطرے کا ڈیٹا',
  'Financial Data / مالی ڈیٹا',
  'Legal Data / قانونی ڈیٹا',
  'Documents / دستاویزات',
  'Photos / تصاویر',
  'Activities / سرگرمیاں',
  'Incidents / واقعات',
  'Review / جائزہ',
  'Save / محفوظ کریں',
];

export function PersonWizard() {
  const [currentStep, setCurrentStep] = useState(0);
  const progress = useMemo(() => ((currentStep + 1) / steps.length) * 100, [currentStep]);

  return (
    <div className="rounded-2xl border border-border bg-panel p-6 shadow-glow">
      <div className="mb-5">
        <div className="mb-2 flex items-center justify-between text-sm text-muted">
          <span>{steps[currentStep]}</span>
          <span>{currentStep + 1} / {steps.length}</span>
        </div>
        <div className="h-2 rounded-full bg-slate-700">
          <div className="h-2 rounded-full bg-slate-300 transition-all" style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <label className="space-y-2">
          <span className="text-sm text-muted">Full Name / مکمل نام</span>
          <input className="w-full rounded-xl border bg-background px-4 py-3" placeholder="Enter full legal name" />
        </label>
        <label className="space-y-2">
          <span className="text-sm text-muted">CNIC / شناختی کارڈ</span>
          <input className="w-full rounded-xl border bg-background px-4 py-3" placeholder="XXXXX-XXXXXXX-X" />
        </label>
        <label className="space-y-2">
          <span className="text-sm text-muted">Risk Level / خطرہ</span>
          <select className="w-full rounded-xl border bg-background px-4 py-3">
            <option>LOW</option>
            <option>MEDIUM</option>
            <option>HIGH</option>
            <option>CRITICAL</option>
          </select>
        </label>
        <label className="space-y-2">
          <span className="text-sm text-muted">Risk Score / اسکور</span>
          <input type="number" min={0} max={100} className="w-full rounded-xl border bg-background px-4 py-3" placeholder="0 - 100" />
        </label>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <button disabled={currentStep === 0} onClick={() => setCurrentStep((s) => Math.max(0, s - 1))} className="rounded-xl border px-4 py-2 disabled:opacity-40">Previous</button>
        <button onClick={() => setCurrentStep((s) => Math.min(steps.length - 1, s + 1))} className="rounded-xl bg-slate-200 px-4 py-2 text-slate-900">Next</button>
      </div>
    </div>
  );
}
