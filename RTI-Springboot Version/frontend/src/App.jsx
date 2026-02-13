import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Landing from './pages/Landing';
import Workspace from './pages/Workspace';
import Templates from './pages/Templates';
import Docs from './pages/Docs';
import Community from './pages/Community';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-warm font-sans text-gray-900 relative">
        {/* Texture Overlay */}
        <div className="fixed inset-0 pointer-events-none opacity-50 bg-grain z-0"></div>

        <Header />

        <main className="flex-grow pt-20 relative z-10">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/generate" element={<Workspace />} />
            <Route path="/templates" element={<Templates />} />
            <Route path="/docs" element={<Docs />} />
            <Route path="/community" element={<Community />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;
