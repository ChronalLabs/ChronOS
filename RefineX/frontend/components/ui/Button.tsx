import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
}

export function Button({ children, variant = 'primary', className = "", ...props }: ButtonProps) {
  const base = "px-4 py-2 rounded-lg font-medium transition cursor-pointer flex justify-center items-center gap-2";
  const styles = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 shadow-sm",
    secondary: "bg-gray-100 text-gray-800 hover:bg-gray-200",
    outline: "border border-gray-200 text-gray-700 hover:bg-gray-50"
  };
  return (
    <button className={`${base} ${styles[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
