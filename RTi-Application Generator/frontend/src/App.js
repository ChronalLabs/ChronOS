import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Layouts
import MainLayout from './layouts/MainLayout/MainLayout';

// Pages
import Home from './pages/Home/Home';
import GuidedMode from './pages/GuidedMode/GuidedMode';
import AssistedMode from './pages/AssistedMode/AssistedMode';
import Templates from './pages/Templates/Templates';

import './App.css';

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="App">
        <MainLayout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/guided" element={<GuidedMode />} />
            <Route path="/assisted" element={<AssistedMode />} />
            <Route path="/templates" element={<Templates />} />
          </Routes>
        </MainLayout>
        <ToastContainer position="bottom-right" />
      </div>
    </Router>
  );
}

export default App;
