export function Loader({ text = "Loading..." }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center p-12">
      <div className="w-12 h-12 border-4 border-blue-100 border-t-blue-600 rounded-full animate-spin shadow-sm"></div>
      <p className="mt-4 text-gray-500 font-medium animate-pulse">{text}</p>
    </div>
  );
}
