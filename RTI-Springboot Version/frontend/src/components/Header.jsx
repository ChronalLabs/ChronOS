import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Button from './Button';

const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3">
                        <img src="/chronos-logo.jpg" alt="ChronOs Logo" className="w-10 h-10 rounded-lg object-contain" />
                        <div className="flex flex-col">
                            <span className="font-sans font-bold text-xl text-indigo-deep tracking-tight">RTI-Gen</span>
                            <span className="text-[10px] text-gray-500 font-medium uppercase tracking-wider">By ChronOs</span>
                        </div>
                    </Link>

                    {/* Desktop Nav */}
                    <nav className="hidden md:flex items-center gap-8">
                        <Link to="/#features" className="text-gray-600 hover:text-indigo-deep font-medium text-sm transition-colors">Features</Link>
                        <Link to="/templates" className="text-gray-600 hover:text-indigo-deep font-medium text-sm transition-colors">Templates</Link>
                        <Link to="/docs" className="text-gray-600 hover:text-indigo-deep font-medium text-sm transition-colors">Docs</Link>
                        <Link to="/community" className="text-gray-600 hover:text-indigo-deep font-medium text-sm transition-colors">Community</Link>
                    </nav>

                    {/* Actions */}
                    <div className="hidden md:flex items-center gap-4">

                        <Button variant="primary" className="py-2 px-5 text-sm" to="/generate">
                            Generate RTI
                        </Button>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="md:hidden">
                        <button
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            className="p-2 text-gray-600 hover:text-indigo-deep focus:outline-none"
                        >
                            <span className="sr-only">Open menu</span>
                            {/* Hamburger Icon */}
                            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMenuOpen && (
                <div className="md:hidden bg-white border-t border-gray-100 animate-fade-in">
                    <div className="px-4 pt-2 pb-6 space-y-2">
                        <Link to="/#features" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50">Features</Link>
                        <Link to="/templates" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50">Templates</Link>
                        <Link to="/docs" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50">Docs</Link>
                        <Link to="/community" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50">Community</Link>
                        <div className="pt-4 mt-4 border-t border-gray-100">
                            <Button variant="primary" className="w-full justify-center" to="/generate">Generate RTI</Button>
                        </div>
                    </div>
                </div>
            )}
        </header>
    );
};

export default Header;
