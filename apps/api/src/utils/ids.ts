export function buildSequentialId(prefix: string, count: number): string {
  return `${prefix}${String(count).padStart(6, '0')}`;
}
