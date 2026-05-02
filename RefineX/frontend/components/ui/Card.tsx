export function Card({ children, className = "" }: { children: React.ReactNode, className?: string }) {
  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-100 p-6 ${className}`}>
      {children}
    </div>
  );
}
