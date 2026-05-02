'use client'
import DashboardLayout from '@/components/layout/DashboardLayout';
import { DataTable } from '@/components/ui/DataTable';
import { Loader } from '@/components/ui/Loader';
import { getDatasetPreview } from '@/services/api';
import { DatasetPreviewResponse } from '@/types';
import { useEffect, useState } from 'react';
import { Search } from 'lucide-react';

export default function PreviewPage() {
  const [data, setData] = useState<DatasetPreviewResponse | null>(null);

  useEffect(() => {
    getDatasetPreview().then(setData).catch(console.error);
  }, []);

  return (
    <DashboardLayout>
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 tracking-tight">Dataset Preview</h1>
          <p className="text-gray-500 mt-2 text-lg">Live tabular mapping of your uploaded structures.</p>
        </div>
        {data && (
           <div className="relative">
             <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
             <input type="text" placeholder="Search rows..." className="pl-10 pr-4 py-2 border border-gray-200 rounded-lg outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition w-full md:w-64" />
           </div>
        )}
      </div>
      
      {!data ? <Loader text="Loading preview mappings..." /> : (
        <div className="animate-in fade-in duration-500">
           <div className="bg-white p-4 rounded-t-xl border border-b-0 border-gray-200 flex justify-between items-center">
              <span className="font-semibold text-gray-700">Total Valid Rows</span>
              <span className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-bold">{data.totalRows.toLocaleString()}</span>
           </div>
           <DataTable columns={data.columns} data={data.rows} />
        </div>
      )}
    </DashboardLayout>
  );
}
