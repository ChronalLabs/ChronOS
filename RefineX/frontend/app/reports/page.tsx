'use client'
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { DownloadCloud, CheckCircle2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { getReport } from '@/services/api';
import { Loader } from '@/components/ui/Loader';

export default function ReportsPage() {
  const [report, setReport] = useState<any>(null);

  useEffect(() => {
    getReport().then(setReport).catch(console.error);
  }, []);

  return (
    <DashboardLayout>
       <div className="mb-10">
        <h1 className="text-4xl font-bold text-gray-900 tracking-tight">Reports & Generation</h1>
        <p className="text-gray-500 mt-2 text-lg">Retrieve fully formatted diagnostic intelligence reports.</p>
      </div>

      {!report ? <Loader text="Generating secure reports..." /> : (
        <Card className="max-w-3xl animate-in slide-in-from-bottom-4 duration-500 p-8 shadow-md border-gray-200">
          <div className="flex items-center gap-5 mb-8 pb-8 border-b border-gray-100">
             <div className="w-20 h-20 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-600 shadow-inner">
                <CheckCircle2 size={40} />
             </div>
             <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-1">Diagnostic Summary Ready</h2>
                <p className="text-gray-500 text-lg">Report ID: <span className="font-mono text-gray-700 font-medium bg-gray-100 px-2 py-1 rounded">{report.reportId}</span></p>
             </div>
          </div>
          
          <div className="bg-[#F8FAFC] p-8 rounded-2xl border border-gray-200 mb-10 shadow-sm relative overflow-hidden">
            <div className="absolute top-0 left-0 w-2 h-full bg-blue-500"></div>
            <h4 className="font-bold text-gray-900 mb-3 uppercase tracking-wider text-sm">Executive Summary</h4>
            <p className="text-gray-700 italic text-lg leading-relaxed text-blue-900/80">"{report.summary}"</p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4">
             <Button className="flex-1 rounded-xl h-14 text-lg">
               <DownloadCloud className="mr-3" size={22} />
               Download PDF
             </Button>
             <Button variant="outline" className="flex-1 rounded-xl h-14 text-lg bg-gray-50">
               <DownloadCloud className="mr-3" size={22} />
               Export as CSV
             </Button>
          </div>
        </Card>
      )}
    </DashboardLayout>
  );
}
