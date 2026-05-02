'use client'
import { useState } from "react";
import Sidebar from "./Sidebar";
import { Menu } from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-[#F8FAFC] text-gray-900 font-sans relative">
      {/* Mobile Header */}
      <div className="md:hidden flex items-center justify-between bg-white border-b border-gray-200 p-4 sticky top-0 z-30 shadow-sm">
        <div className="font-bold text-xl text-blue-600">AI DataPlatform</div>
        <button onClick={() => setSidebarOpen(true)} className="p-2 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-700 transition">
          <Menu size={24} />
        </button>
      </div>

      {/* Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-gray-900/40 z-40 md:hidden backdrop-blur-sm transition-opacity" 
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <div className={`fixed inset-y-0 left-0 transform ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} md:relative md:translate-x-0 transition duration-300 ease-in-out z-50 md:z-0 md:flex h-full`}>
         <Sidebar onClose={() => setSidebarOpen(false)} />
      </div>

      <main className="flex-1 p-4 md:p-8 h-full md:h-screen w-full md:overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
