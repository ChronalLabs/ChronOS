'use client'
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, FileSpreadsheet, BarChart2, FileText, Settings, X } from 'lucide-react';
import clsx from 'clsx';

const navItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Preview', href: '/preview', icon: FileSpreadsheet },
  { name: 'Analysis', href: '/analysis', icon: BarChart2 },
  { name: 'Reports', href: '/reports', icon: FileText },
];

export default function Sidebar({ onClose }: { onClose?: () => void }) {
  const pathname = usePathname();
  
  return (
    <aside className="w-64 bg-white border-r min-h-screen flex flex-col shadow-sm sticky top-0 h-full">
      <div className="p-4 border-b font-bold text-xl text-blue-600 h-16 flex items-center justify-between md:justify-center">
        <span>AI DataPlatform</span>
        {onClose && (
          <button onClick={onClose} className="md:hidden p-1 text-gray-500 hover:bg-gray-100 rounded-md">
            <X size={20} />
          </button>
        )}
      </div>
      <nav className="flex-1 p-4 space-y-2 mt-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link 
              key={item.name} 
              href={item.href} 
              onClick={onClose}
              className={clsx("flex items-center gap-3 px-4 py-3 rounded-lg transition", isActive ? "bg-blue-50 text-blue-600 font-medium" : "text-gray-600 hover:bg-gray-50 hover:text-gray-900")}
            >
              <Icon size={20} />
              {item.name}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-gray-100">
        <Link href="/" className="flex items-center gap-3 px-4 py-3 text-gray-500 hover:bg-gray-50 hover:text-gray-900 rounded-lg transition">
          <Settings size={20} />
          Exit to Landing
        </Link>
      </div>
    </aside>
  );
}
