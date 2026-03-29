import { Topbar } from '@/components/topbar';
import { PersonWizard } from '@/components/person-wizard';

export default function PersonsPage() {
  return (
    <div>
      <Topbar title="Person Registry / افراد رجسٹری" subtitle="Create and manage subject individual records with bilingual enterprise fields." />
      <PersonWizard />
    </div>
  );
}
