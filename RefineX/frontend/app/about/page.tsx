import Navbar from '@/components/layout/Navbar';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Navbar />
      <main className="max-w-4xl mx-auto py-20 px-8">
         <h1 className="text-5xl font-extrabold mb-8 text-center text-gray-900 tracking-tight">About the Project</h1>
         <div className="w-24 h-1 bg-blue-600 mx-auto mb-12 rounded-full"></div>
         
         <Card className="p-12 mb-12 shadow-md">
           <h2 className="text-3xl font-bold mb-6 text-gray-900">Our Mission</h2>
           <p className="text-gray-600 mb-10 text-xl leading-relaxed">
             Welcome to the AI Data Intelligence Platform. Our core mission is to empower businesses and researchers by automating the tedious process of dataset cleaning and generating rich, statistical insights seamlessly. 
           </p>
           
           <h2 className="text-3xl font-bold mb-6 text-gray-900">Under the Hood</h2>
           <p className="text-gray-600 text-xl leading-relaxed">
             This platform leverages cutting-edge technologies including React 18, Next.js App Router, FastAPI backend, and robust Mock integrations acting as powerful placeholders for upcoming complex machine learning algorithms. The UI utilizes Tailwind CSS for maximum responsiveness and aesthetics.
           </p>
         </Card>
         
         <div className="text-center p-8 bg-blue-50 rounded-3xl border border-blue-100">
            <h3 className="text-2xl font-bold mb-6 text-blue-900">Ready to test our pipeline?</h3>
            <Link href="/dashboard">
              <Button className="rounded-xl px-10 h-14 text-lg font-bold shadow-sm hover:shadow-lg transition-shadow bg-blue-600 hover:bg-blue-700">Launch Platform Dashboard</Button>
            </Link>
         </div>
      </main>
    </div>
  );
}
