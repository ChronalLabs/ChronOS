import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import RightPanel from "../components/RightPanel";
import { History, Menu, Delete } from "lucide-react";

// Safe Math Evaluation
const evaluateMath = (expr) => {
  if (!expr) return "";
  try {
    let toEval = expr
      .replace(/×/g, "*")
      .replace(/÷/g, "/")
      .replace(/-/g, "-")
      .replace(/p/g, "Math.PI")
      .replace(/e/g, "Math.E")
      .replace(/sin\(/g, "Math.sin(")
      .replace(/cos\(/g, "Math.cos(")
      .replace(/tan\(/g, "Math.tan(")
      .replace(/log\(/g, "Math.log10(")
      .replace(/ln\(/g, "Math.log(")
      .replace(/v\(/g, "Math.sqrt(")
      .replace(/\^/g, "**")
      .replace(/%/g, "/100");
    
    // Add missing closing parentheses
    const openParen = (toEval.match(/\(/g) || []).length;
    const closeParen = (toEval.match(/\)/g) || []).length;
    for(let i = 0; i < openParen - closeParen; i++) {
        toEval += ")";
    }

    const res = new Function(`return ${toEval}`)();
    if (res === Infinity || res === -Infinity) return "Error";
    if (isNaN(res) || res === undefined) return "Error";
    
    // Format to avoid long decimals
    return parseFloat(res.toFixed(8)).toString();
  } catch (err) {
    return "Error";
  }
};

const Calculator = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [scientificMode, setScientificMode] = useState(true);

  const [expression, setExpression] = useState("");
  const [result, setResult] = useState("0");
  const [lastExpression, setLastExpression] = useState("1250 * 0.15");

  const [historyItems, setHistoryItems] = useState([
    { id: 1, title: 'PHYSICS LAB #2', time: '2 mins ago', expression: '1250 * 0.15', result: '187.5' },
    { id: 2, title: 'MATH HOMEWORK', time: '15 mins ago', expression: 'v(144) + 5^2', result: '37' },
    { id: 3, title: 'PROJECT BUDGET', time: '1 hour ago', expression: '450 / 3 * 12', result: '1800' },
    { id: 4, title: 'STUDY GROUP EXP', time: 'Yesterday', expression: '89.90 + 12.50 + 5.00', result: '107.40' }
  ]);

  // Live evaluation effect for real-time result preview
  useEffect(() => {
    if (expression) {
        const res = evaluateMath(expression);
        if (res !== "Error") {
            setResult(res);
        } else {
            setResult("...");
        }
    } else {
        setResult("0");
    }
  }, [expression]);

  const handleButtonClick = (btn) => {
    if (btn.label === 'C') {
        setExpression("");
        setResult("0");
        return;
    }
    if (btn.label === '?') {
        setExpression(prev => prev.length > 0 ? prev.slice(0, -1) : "");
        return;
    }
    if (btn.label === '=') {
        if (!expression) return;
        const res = evaluateMath(expression);
        setResult(res);
        if (res !== "Error" && res !== "...") {
            const newHistory = {
                id: Date.now(),
                title: 'CALCULATION',
                time: 'Just now',
                expression: expression,
                result: res
            };
            setHistoryItems(prev => [newHistory, ...prev].slice(0, 10));
            setLastExpression(expression);
            setExpression(res); // Allow chaining calculations
        }
        return;
    }

    let valToAppend = btn.value || btn.label;
    if (btn.action === 'func') valToAppend = btn.label + '(';
    if (btn.action === 'sq') valToAppend = '^2';

    setExpression(prev => prev + valToAppend);
  };

  const handlePreset = (val) => {
    setExpression(prev => prev + val);
  };

  const clearHistory = () => setHistoryItems([]);

  // Button Grid Configuration
  const sciColor = 'hidden md:flex bg-background text-text-secondary font-semibold hover:bg-border/50';
  const numColor = 'bg-background text-text-main font-bold text-xl hover:bg-border/50';
  const opColor = 'bg-background text-primary font-semibold text-xl hover:bg-primary/10';

  const buttons = scientificMode 
    ? [
        { label: 'sin', action: 'func', color: sciColor }, { label: 'cos', action: 'func', color: sciColor }, 
        { label: 'C', color: 'bg-background text-red-500 font-semibold hover:bg-red-50' }, { label: '?', icon: <Delete size={20} />, color: 'bg-background text-primary hover:bg-primary/10' }, { label: '%', color: opColor }, { label: '÷', color: opColor },
        
        { label: 'tan', action: 'func', color: sciColor }, { label: 'log', action: 'func', color: sciColor }, 
        { label: '7', color: numColor }, { label: '8', color: numColor }, { label: '9', color: numColor }, { label: '×', color: opColor },
        
        { label: 'ln', action: 'func', color: sciColor }, { label: 'v', action: 'func', color: sciColor }, 
        { label: '4', color: numColor }, { label: '5', color: numColor }, { label: '6', color: numColor }, { label: '-', color: 'bg-background text-primary font-semibold text-3xl pb-1 hover:bg-primary/10' },
        
        { label: 'x²', action: 'sq', color: sciColor }, { label: '^', action: 'pow', color: sciColor }, 
        { label: '1', color: numColor }, { label: '2', color: numColor }, { label: '3', color: numColor }, { label: '+', color: 'bg-background text-primary font-semibold text-2xl hover:bg-primary/10' },
        
        { label: 'p', action: 'val', color: sciColor }, { label: 'e', action: 'val', color: sciColor }, 
        { label: '0', color: numColor }, { label: '.', color: numColor }, { label: '=', color: 'bg-primary text-white font-bold text-2xl hover:bg-primary-dark shadow-[0_8px_16px_rgba(16,185,129,0.3)]', classes: 'col-span-2' }
      ]
    : [
        { label: 'C', color: 'bg-background text-red-500 font-semibold hover:bg-red-50' }, { label: '?', icon: <Delete size={20} />, color: 'bg-background text-primary hover:bg-primary/10' }, { label: '%', color: opColor }, { label: '÷', color: opColor },
        
        { label: '7', color: numColor }, { label: '8', color: numColor }, { label: '9', color: numColor }, { label: '×', color: opColor },
        
        { label: '4', color: numColor }, { label: '5', color: numColor }, { label: '6', color: numColor }, { label: '-', color: 'bg-background text-primary font-semibold text-3xl pb-1 hover:bg-primary/10' },
        
        { label: '1', color: numColor }, { label: '2', color: numColor }, { label: '3', color: numColor }, { label: '+', color: 'bg-background text-primary font-semibold text-2xl hover:bg-primary/10' },
        
        { label: '0', color: numColor, classes: 'col-span-2' }, { label: '.', color: numColor }, { label: '=', color: 'bg-primary text-white font-bold text-2xl hover:bg-primary-dark shadow-[0_8px_16px_rgba(16,185,129,0.3)]' }
      ];

  return (
    <div className="flex bg-background min-h-screen text-text-main font-sans overflow-hidden">
      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div
          onClick={() => setIsSidebarOpen(false)}
          className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm"
        />
      )}

      {/* Left Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
      </div>

      {/* Main Content Area Wrapper */}
      <div className="flex-1 flex flex-col md:ml-20 xl:mr-80 min-h-screen relative transition-all duration-300 z-10">
        
        {/* Main Content */}
        <main className="flex-1 p-6 md:p-8 overflow-y-auto w-full max-w-[1400px] mx-auto space-y-8">
          
          {/* Header */}
          <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50 md:hidden"
              >
                <Menu size={24} />
              </button>
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-text-main">Study Calculator</h1>
                <p className="text-sm text-text-secondary mt-1">Quick calculations for your research and labs</p>
              </div>
            </div>
            <div className="flex items-center gap-2 bg-surface px-4 py-2 rounded-full shadow-sm border border-border/50">
              <div className="w-2 h-2 bg-primary rounded-full"></div>
              <span className="text-sm font-medium text-text-secondary">Focus Mode: Physics Lab</span>
            </div>
          </header>

          {/* Calculator Layout */}
          <div className="flex flex-col xl:flex-row gap-8">
            
            {/* Left Box (Calculator) */}
            <div className="flex-1 bg-surface rounded-[2rem] p-6 lg:p-10 shadow-card border border-border/50 flex flex-col">
              
              {/* Display Area */}
              <div className="flex flex-col items-end mb-8 relative min-h-[120px]">
                {/* Scientific toggle */}
                <div className="absolute top-0 left-0 flex items-center gap-3">
                    <span className="text-xs font-bold text-text-muted tracking-widest uppercase">Scientific Mode</span>
                    <button 
                      onClick={() => setScientificMode(!scientificMode)}
                      className={`relative w-11 h-6 rounded-full transition-colors ${scientificMode ? 'bg-primary' : 'bg-border'}`}
                    >
                      <span className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${scientificMode ? 'left-6' : 'left-1'}`}></span>
                    </button>
                </div>
                
                <div className="text-lg text-text-secondary tracking-widest font-medium mt-10 md:mt-0 h-8 flex items-end break-all text-right">
                    {expression || lastExpression}
                </div>
                <div className="text-5xl md:text-6xl font-bold text-text-main mt-2 tracking-tight overflow-hidden break-all max-w-full">
                    {result}
                </div>
              </div>

              {/* Number Pad Grid */}
              <div className={`grid gap-3 md:gap-4 w-full flex-1 ${scientificMode ? 'grid-cols-4 md:grid-cols-6' : 'grid-cols-4'}`}>
                {buttons.map((btn, idx) => (
                    <button
                        key={idx}
                        onClick={() => handleButtonClick(btn)}
                        className={`
                          py-3 md:py-5 lg:py-6 rounded-2xl flex items-center justify-center transition-all duration-200 active:scale-95 shadow-sm
                          ${btn.color || 'bg-background hover:bg-border/50 text-text-main'}
                          ${btn.classes ? btn.classes : 'col-span-1'}
                        `}
                    >
                        {btn.icon ? btn.icon : btn.label}
                    </button>
                ))}
              </div>
            </div>

            {/* Right Stack (History & Presets) */}
            <div className="w-full xl:w-[400px] flex flex-col gap-6">
              
              {/* History Section */}
              <div className="flex-1 flex flex-col">
                <div className="flex items-center justify-between mb-4 px-2">
                  <div className="flex items-center gap-2">
                    <History size={20} className="text-text-main" />
                    <h2 className="text-xl font-bold text-text-main">History</h2>
                  </div>
                  <button onClick={clearHistory} className="text-sm font-semibold text-text-muted hover:text-text-secondary transition-colors">Clear All</button>
                </div>

                <div className="flex flex-col gap-4 overflow-y-auto max-h-[500px] custom-scrollbar pr-2">
                  {historyItems.length === 0 ? (
                      <div className="text-center p-8 text-text-muted text-sm font-medium">No calculation history</div>
                  ) : (
                      historyItems.map((item, index) => (
                        <div 
                            key={item.id} 
                            onClick={() => setExpression(item.result)}
                            className={`p-5 rounded-2xl shadow-sm border transition-all cursor-pointer group
                                ${index === 0 ? 'bg-surface border-primary/20 shadow-card hover:shadow-soft' : 'bg-surface border-border/50 hover:shadow-soft'}
                            `}
                        >
                            <div className="flex justify-between items-center mb-2">
                            <span className="text-xs font-bold text-text-muted tracking-widest">{item.title}</span>
                            <span className="text-xs font-medium text-text-muted">{item.time}</span>
                            </div>
                            <div className="flex justify-between items-end">
                            <span className="text-text-secondary font-medium tracking-wide truncate max-w-[180px]">{item.expression}</span>
                            <span className={`text-xl font-bold ${index === 0 ? 'text-primary' : 'text-text-main'}`}>
                                {item.result}
                            </span>
                            </div>
                        </div>
                      ))
                  )}
                </div>
              </div>

              {/* Scientific Presets */}
              <div className="bg-primary/5 rounded-[2rem] p-6 border border-primary/10">
                <h3 className="text-sm font-bold text-text-main mb-4">Scientific Presets</h3>
                <div className="grid grid-cols-2 gap-3">
                  <button onClick={() => handlePreset('p')} className="bg-surface py-3 px-4 rounded-xl text-sm font-semibold text-text-main shadow-sm hover:shadow hover:text-primary transition-all flex items-center justify-center">
                    Pi (p)
                  </button>
                  <button onClick={() => handlePreset('e')} className="bg-surface py-3 px-4 rounded-xl text-sm font-semibold text-text-main shadow-sm hover:shadow hover:text-primary transition-all flex items-center justify-center">
                    Euler (e)
                  </button>
                  <button onClick={() => handlePreset('9.81')} className="bg-surface py-3 px-4 rounded-xl text-sm font-semibold text-text-main shadow-sm hover:shadow hover:text-primary transition-all flex items-center justify-center">
                    Gravity (g)
                  </button>
                  <button onClick={() => handlePreset('6.626e-34')} className="bg-surface py-3 px-4 rounded-xl text-sm font-semibold text-text-main shadow-sm hover:shadow hover:text-primary transition-all flex items-center justify-center">
                    Planck (h)
                  </button>
                </div>
              </div>

            </div>
          </div>
        
        </main>
      </div>

      {/* Right Panel (Desktop) */}
      <div className="hidden xl:block fixed inset-y-0 right-0 z-40 w-80">
        <RightPanel />
      </div>

    </div>
  );
};

export default Calculator;
