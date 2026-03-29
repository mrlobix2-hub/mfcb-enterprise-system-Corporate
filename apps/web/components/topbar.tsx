export function Topbar({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="mb-8 flex flex-col gap-2 border-b border-border pb-5">
      <h2 className="text-3xl font-semibold">{title}</h2>
      <p className="text-sm text-muted">{subtitle}</p>
    </div>
  );
}
