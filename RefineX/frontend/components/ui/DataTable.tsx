import React from 'react';

export function DataTable({ columns, data }: { columns: string[], data: any[] }) {
  if (!data || data.length === 0) return <div className="p-8 text-center text-gray-500 bg-gray-50 rounded-lg border border-dashed border-gray-200">No data available</div>;

  return (
    <div className="overflow-x-auto bg-white border border-gray-200 rounded-xl shadow-sm">
      <table className="w-full text-sm text-left">
        <thead className="bg-[#F8FAFC] border-b border-gray-100">
          <tr>
            {columns.map((col, index) => (
              <th key={index} className="px-6 py-4 font-semibold text-gray-600 tracking-wider capitalize">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-blue-50/50 transition">
              {columns.map((col, colIndex) => (
                <td key={colIndex} className="px-6 py-4 text-gray-700 whitespace-nowrap">
                  {row[col]?.toString() || '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
