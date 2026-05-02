import { Card } from "./Card";

export function StatCard({ title, value, icon: Icon, trend }: { title: string, value: string | number, icon: any, trend?: string }) {
  return (
    <Card className="flex items-center justify-between hover:shadow-md transition-shadow">
      <div>
        <p className="text-sm text-gray-500 font-medium mb-1">{title}</p>
        <h3 className="text-3xl font-bold text-gray-900">{value}</h3>
        {trend && <p className="text-sm text-green-500 mt-2 font-medium">{trend}</p>}
      </div>
      <div className="w-14 h-14 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
        <Icon size={28} />
      </div>
    </Card>
  );
}
