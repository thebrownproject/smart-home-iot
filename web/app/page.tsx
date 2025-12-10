import { SensorGrid } from "@/components/SensorGrid";
import { ControlPanel } from "@/components/ControlPanel";
import { RecentAccess } from "@/components/RecentAccess";

export default function Home() {
  return (
    <section className="flex flex-col gap-5 py-1 max-w-2xl mx-auto px-4">
      <SensorGrid />
      <ControlPanel />
      <RecentAccess />
    </section>
  );
}
