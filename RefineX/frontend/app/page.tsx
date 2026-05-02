import Navbar from '@/components/layout/Navbar';
import { Button } from '@/components/ui/Button';
import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col">
      <Navbar />
      <main className="flex-1 flex flex-col items-center justify-center text-center p-8 relative overflow-hidden">
        {/* Abstract Background Shapes */}
        <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50 z-0"></div>
        <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50 z-0"></div>

        <div className="z-10 relative">
          <div className="inline-blockpx-4 py-1.5 mb-6 text-sm font-semibold text-blue-600 bg-blue-50 rounded-full border border-blue-100">
            v1.0 is now live 🎉
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 tracking-tight mb-8 leading-tight">
            Intelligent <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Dataset Cleaning</span> <br className="hidden md:block"/> & Analysis System
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload your unstructured datasets and leverage bleeding-edge algorithms to clean, analyze, and generate comprehensive intelligence reports in minutes.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/dashboard">
              <Button className="px-8 py-4 text-lg bg-blue-600 hover:bg-blue-700 shadow-lg font-bold rounded-xl">Get Started for Free</Button>
            </Link>
            <Link href="/about">
              <Button variant="outline" className="px-8 py-4 text-lg bg-white shadow-sm font-bold rounded-xl border-gray-200">Learn More</Button>
            </Link>
          </div>
        </div>
        
        <div className="mt-32 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl w-full z-10">
          {[
            { title: "Automated Cleaning", desc: "Identify and resolve missing values automatically with high accuracy." },
            { title: "Smart Analysis", desc: "Generate insights, correlations, and statistical overviews instantly." },
            { title: "Export Reports", desc: "Download beautifully formatted PDF/CSV management reports." }
          ].map((feat, i) => (
             <div key={i} className="bg-white/80 backdrop-blur-sm p-8 rounded-3xl shadow-sm border border-gray-100 flex flex-col items-center text-center hover:-translate-y-2 transition-transform duration-300">
               <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mb-6 text-2xl font-bold shadow-inner">{i+1}</div>
               <h3 className="text-xl font-bold text-gray-900 mb-3">{feat.title}</h3>
               <p className="text-gray-500 leading-relaxed">{feat.desc}</p>
             </div>
          ))}
        </div>
      </main>
    </div>
  );
}
