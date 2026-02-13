import React from 'react';
import { Link } from 'react-router-dom';

const Button = ({
    children,
    variant = 'primary',
    size = 'md', // Added size prop with default
    className = '',
    to,
    ...props
}) => {

    // The styling logic has been refactored to use conditional classes directly
    // instead of a separate variants object and baseStyles.
    const buttonClasses = `
        inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 active:scale-95
        ${variant === 'primary'
            ? 'bg-indigo-deep text-white hover:bg-black hover:text-white hover:scale-105 shadow-lg hover:shadow-xl'
            : 'bg-white text-indigo-deep border border-gray-200 hover:bg-black hover:text-white hover:border-transparent hover:scale-105 shadow-sm'}
        ${size === 'sm' ? 'px-3 py-1.5 text-sm' : ''}
        ${size === 'md' ? 'px-5 py-2.5 text-base' : ''}
        ${size === 'lg' ? 'px-6 py-3 text-lg' : ''}
        ${className}
      `;

    if (to) {
        return (
            <Link to={to} className={buttonClasses} {...props}>
                {children}
            </Link>
        );
    }

    return (
        <button
            className={buttonClasses}
            {...props}
        >
            {children}
        </button>
    );
};

export default Button;
