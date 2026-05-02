import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between p-4 bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="flex items-center font-bold text-xl text-blue-600">
        <span>AI DataPlatform</span>
      </div>
      <div className="flex items-center gap-6">
        <Link href="/" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition">Landing</Link>
        <Link href="/about" className="text-sm font-medium text-gray-600 hover:text-blue-600 transition">About</Link>
        <Link href="/dashboard" className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition shadow-sm">
          Go to Dashboard
        </Link>
      </div>
    </nav>
  );
}
