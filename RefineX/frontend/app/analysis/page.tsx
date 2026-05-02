'use client'
import DashboardLayout from '@/components/layout/DashboardLayout';
import { StatCard } from '@/components/ui/StatCard';
import { Card } from '@/components/ui/Card';
import { Loader } from '@/components/ui/Loader';
import { getAnalysis } from '@/services/api';
import { AnalysisResponse } from '@/types';
import { useEffect, useState } from 'react';
import { Database, AlertTriangle, Copy, Lightbulb } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function AnalysisPage() {
  const [data, setData] = useState<AnalysisResponse | null>(null);

  useEffect(() => {
    getAnalysis().then(setData).catch(console.error);
  }, []);

  const COLORS = ['#2563eb', '#93c5fd', '#3b82f6'];

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 tracking-tight">Intelligence Analysis</h1>
        <p className="text-gray-500 mt-2 text-lg">Statistical overview and automated insights.</p>
      </div>

      {!data ? <Loader text="Analyzing constraints and statistics..." /> : (
        <div className="space-y-8 animate-in fade-in duration-500">
           {/* Stat Cards */}
           <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
             <StatCard title="Total Records" value={data.stats.totalRecords.toLocaleString()} icon={Database} trend="Complete dataset parsed" />
             <StatCard title="Missing Values" value={data.stats.missingValues.toLocaleString()} icon={AlertTriangle} trend="Successfully Cleansed" />
             <StatCard title="Duplicates Found" value={data.stats.duplicateRows.toLocaleString()} icon={Copy} trend="Removed from scope" />
           </div>

           {/* Charts Grid */}
           <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
             <Card>
               <h3 className="text-lg font-bold mb-6 text-gray-800">Status Distribution</h3>
               <div className="h-72">
                 <ResponsiveContainer width="100%" height="100%">
                   <PieChart>
                     <Pie data={data.charts.pieChart} cx="50%" cy="50%" innerRadius={70} outerRadius={100} paddingAngle={5} dataKey="value">
                       {data.charts.pieChart.map((entry: any, index: number) => (
                         <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                       ))}
                     </Pie>
                     <Tooltip />
                   </PieChart>
                 </ResponsiveContainer>
               </div>
             </Card>

             <Card>
               <h3 className="text-lg font-bold mb-6 text-gray-800">Monthly Trends</h3>
               <div className="h-72">
                 <ResponsiveContainer width="100%" height="100%">
                   <BarChart data={data.charts.barChart}>
                     <XAxis dataKey="name" stroke="#9ca3af" />
                     <YAxis stroke="#9ca3af" />
                     <Tooltip cursor={{fill: '#f8fafc'}} />
                     <Bar dataKey="value" fill="#2563eb" radius={[6, 6, 0, 0]} />
                   </BarChart>
                 </ResponsiveContainer>
               </div>
             </Card>
           </div>
           
           <Card className="bg-gradient-to-br from-indigo-50 to-blue-50 border-blue-100 shadow-sm">
             <h3 className="text-xl font-bold mb-6 flex items-center gap-3 text-blue-900">
               <Lightbulb className="text-blue-600" /> Key Generated Insights
             </h3>
             <ul className="space-y-4">
               {data.insights.map((insight, idx) => (
                 <li key={idx} className="flex items-start gap-4 bg-white p-5 rounded-xl shadow-sm border border-blue-50 hover:shadow-md transition">
                   <span className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-bold text-sm flex-shrink-0">{idx+1}</span>
                   <p className="text-gray-700 leading-relaxed font-medium">{insight}</p>
                 </li>
               ))}
             </ul>
           </Card>
        </div>
      )}
    </DashboardLayout>
  );
}
