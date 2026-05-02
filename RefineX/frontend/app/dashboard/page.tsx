'use client'
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { UploadCloud, CheckCircle2, FileSpreadsheet } from 'lucide-react';
import { useState } from 'react';
import { uploadDataset } from '@/services/api';
import Link from 'next/link';

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<'idle' | 'uploading' | 'done'>('idle');
  const [result, setResult] = useState<any>(null);

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    try {
      const res = await uploadDataset(file);
      setResult(res);
      setStatus('done');
    } catch (e) {
      console.error(e);
      setStatus('idle');
    }
  }

  return (
    <DashboardLayout>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 tracking-tight">Dashboard Overview</h1>
        <p className="text-gray-500 mt-2 text-lg">Upload data to initiate your intelligence workflow.</p>
      </div>
      
      <div className="grid grid-cols-1 gap-8">
        <Card className={`p-16 flex flex-col items-center justify-center text-center border-dashed border-2 transition-all duration-300 ${status === 'uploading' ? 'border-blue-400 bg-blue-50' : 'border-gray-200 hover:border-blue-400 bg-white'}`}>
           {status === 'done' ? (
             <div className="flex flex-col items-center animate-in fade-in zoom-in duration-500">
               <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6">
                 <CheckCircle2 size={40} className="text-green-600" />
               </div>
               <h3 className="text-2xl font-bold text-gray-900 mb-2">Upload Successful</h3>
               <p className="text-gray-500 mb-8 max-w-md">File <span className="font-semibold text-gray-700">"{result?.fileName}"</span> was completely processed and verified. Extracted {result?.rows} rows.</p>
               <Button onClick={() => { setStatus('idle'); setFile(null); }} variant="outline" className="rounded-xl">Upload Another Dataset</Button>
             </div>
           ) : (
             <div className="flex flex-col items-center w-full max-w-lg">
               <div className="w-20 h-20 bg-blue-50 rounded-full flex items-center justify-center mb-6 shadow-inner">
                 <UploadCloud size={40} className="text-blue-600" />
               </div>
               <h3 className="text-2xl font-bold text-gray-900 mb-2">Upload Dataset</h3>
               <p className="text-gray-500 mb-8">Drag and drop your CSV or Excel files, or click to select.</p>
               
               <input 
                 type="file" 
                 accept=".csv" 
                 onChange={(e) => setFile(e.target.files?.[0] || null)}
                 className="hidden" 
                 id="fileUpload" 
               />
               <label htmlFor="fileUpload" className="w-full mb-4">
                 <div className="w-full h-14 border border-gray-200 rounded-xl flex items-center px-4 cursor-pointer hover:bg-gray-50 transition shadow-sm">
                   <FileSpreadsheet size={20} className="text-gray-400 mr-3" />
                   <span className="text-gray-600 flex-1 text-left truncate">{file ? file.name : "Select a valid (.csv) file..."}</span>
                 </div>
               </label>
               
               <div className="w-full flex justify-end">
                 <Button onClick={handleUpload} disabled={!file || status === 'uploading'} className="rounded-xl w-full h-12 text-lg">
                   {status === 'uploading' ? (
                     <div className="flex items-center gap-2">
                       <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                       Processing...
                     </div>
                   ) : 'Confirm & Upload'}
                 </Button>
               </div>
             </div>
           )}
        </Card>

        {status === 'done' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in slide-in-from-bottom-8 duration-700">
            <Card className="hover:border-blue-200 transition">
               <h3 className="font-bold text-xl mb-2 text-gray-900">Quick Actions</h3>
               <p className="text-gray-500 mb-6">View the detailed tabular breakdown of the current dataset mapping.</p>
               <Link href="/preview"><Button className="w-full rounded-xl">Go to Data Preview</Button></Link>
            </Card>
            <Card className="hover:border-purple-200 transition">
               <h3 className="font-bold text-xl mb-2 text-gray-900">Deep Insights</h3>
               <p className="text-gray-500 mb-6">Analyze correlations, detect missing values, and review charts.</p>
               <Link href="/analysis"><Button variant="outline" className="w-full rounded-xl border-gray-200">View Advanced Analysis</Button></Link>
            </Card>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
