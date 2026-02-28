import React, { useState, useRef, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import { Menu, PenTool, Eraser, Download, Undo2, Redo2, ZoomIn, Image as ImageIcon, AlignLeft, Cloud, Sparkles, MoreVertical } from "lucide-react";

const DrawingPad = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  
  const [isDrawing, setIsDrawing] = useState(false);
  const [tool, setTool] = useState("pen"); // 'pen', 'highlighter', 'eraser'
  const [color, setColor] = useState("#10B981"); // Default primary green
  const [lineWidth, setLineWidth] = useState(5);
  
  const [history, setHistory] = useState([]);
  const [historyStep, setHistoryStep] = useState(-1);
  const [hasDrawn, setHasDrawn] = useState(false);

  // Initialize Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const parent = canvas.parentElement;
    
    // Set actual responsive constraints without losing definition
    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight;
    
    const ctx = canvas.getContext("2d");
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    contextRef.current = ctx;

    // Save initial blank state
    saveHistoryState(canvas);

    // Make canvas responsive on window resize
    const handleResize = () => {
      const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      canvas.width = parent.clientWidth;
      canvas.height = parent.clientHeight;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      contextRef.current = ctx;
      if (imgData) ctx.putImageData(imgData, 0, 0);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const saveHistoryState = (canvas) => {
    const dataUrl = canvas.toDataURL();
    const newHistory = history.slice(0, historyStep + 1);
    newHistory.push(dataUrl);
    setHistory(newHistory);
    setHistoryStep(newHistory.length - 1);
  };

  const getCoordinates = (e) => {
    if (e.touches && e.touches.length > 0) {
      const rect = canvasRef.current.getBoundingClientRect();
      return {
        offsetX: e.touches[0].clientX - rect.left,
        offsetY: e.touches[0].clientY - rect.top,
      };
    }
    return {
      offsetX: e.nativeEvent.offsetX,
      offsetY: e.nativeEvent.offsetY,
    };
  };

  const startDrawing = (e) => {
    const { offsetX, offsetY } = getCoordinates(e);
    
    // Switch composition mode depending on tool
    if (tool === 'eraser') {
      contextRef.current.globalCompositeOperation = 'destination-out';
      contextRef.current.lineWidth = lineWidth * 4;
    } else if (tool === 'highlighter') {
      contextRef.current.globalCompositeOperation = 'source-over';
      contextRef.current.globalAlpha = 0.4;
      contextRef.current.strokeStyle = color;
      contextRef.current.lineWidth = lineWidth * 3;
    } else {
      contextRef.current.globalCompositeOperation = 'source-over';
      contextRef.current.globalAlpha = 1.0;
      contextRef.current.strokeStyle = color;
      contextRef.current.lineWidth = lineWidth;
    }

    contextRef.current.beginPath();
    contextRef.current.moveTo(offsetX, offsetY);
    setIsDrawing(true);
    if (!hasDrawn) setHasDrawn(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    e.preventDefault(); // Prevent scrolling on touch devices
    const { offsetX, offsetY } = getCoordinates(e);
    contextRef.current.lineTo(offsetX, offsetY);
    contextRef.current.stroke();
  };

  const endDrawing = () => {
    if (!isDrawing) return;
    contextRef.current.closePath();
    setIsDrawing(false);
    saveHistoryState(canvasRef.current);
  };

  const handleUndo = () => {
    if (historyStep > 0) {
      const newStep = historyStep - 1;
      setHistoryStep(newStep);
      restoreCanvas(history[newStep]);
    } else if (historyStep === 0) {
        // clear canvas back to state 0
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        setHasDrawn(false);
    }
  };

  const handleRedo = () => {
    if (historyStep < history.length - 1) {
      const newStep = historyStep + 1;
      setHistoryStep(newStep);
      restoreCanvas(history[newStep]);
      setHasDrawn(true);
    }
  };

  const restoreCanvas = (dataUrl) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const img = new Image();
    img.src = dataUrl;
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1.0;
      ctx.drawImage(img, 0, 0);
    };
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    saveHistoryState(canvas);
    setHasDrawn(false);
  };

  const exportCanvas = () => {
    const canvas = canvasRef.current;
    
    // Create an offscreen canvas to put a white background
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const ctx = tempCanvas.getContext("2d");
    
    // Draw white background
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // Draw the actual canvas content on top
    ctx.drawImage(canvas, 0, 0);

    const link = document.createElement("a");
    link.download = "study_sketch.png";
    link.href = tempCanvas.toDataURL("image/png");
    link.click();
  };

  // Pre-defined colors matching UI
  const colors = ["#10B981", "#EC4899", "#3B82F6", "#F59E0B", "#1F2937"];
  const linePicks = [2, 5, 10];

  return (
    <div className="flex bg-background min-h-screen text-text-main font-sans overflow-hidden">
      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div onClick={() => setIsSidebarOpen(false)} className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm" />
      )}

      {/* Left Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
      </div>

      {/* Main Content Area (Dynamic padding for right static Gallery panel) */}
      <div className="flex-1 flex flex-col md:ml-20 xl:mr-[340px] min-h-screen relative transition-all duration-300 z-10 z-0">
        
        {/* Mobile menu trigger */}
        <div className="md:hidden p-4 absolute top-0 left-0 z-20">
            <button onClick={() => setIsSidebarOpen(true)} className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50 shadow-sm">
                <Menu size={24} />
            </button>
        </div>

        {/* Top Floating Toolbar */}
        <div className="absolute top-6 left-1/2 -translate-x-1/2 z-20 flex bg-surface p-2 rounded-full shadow-card border border-border/50 items-center gap-2 overflow-x-auto max-w-[90vw] custom-scrollbar">
            
            {/* Tools */}
            <div className="flex bg-background rounded-full p-1 border border-border/50 shadow-inner">
                <button 
                  onClick={() => setTool('pen')}
                  className={`p-2.5 rounded-full transition-all ${tool === 'pen' ? 'bg-surface text-primary shadow-soft' : 'text-text-muted hover:text-text-main'}`}
                >
                    <PenTool size={18} />
                </button>
                <button 
                  onClick={() => setTool('highlighter')}
                  className={`p-2.5 rounded-full transition-all ${tool === 'highlighter' ? 'bg-surface text-primary shadow-soft' : 'text-text-muted hover:text-text-main'}`}
                >
                    <AlignLeft size={18} />
                </button>
                <button 
                  onClick={() => setTool('eraser')}
                  className={`p-2.5 rounded-full transition-all ${tool === 'eraser' ? 'bg-surface text-primary shadow-soft' : 'text-text-muted hover:text-text-main'}`}
                >
                    <Eraser size={18} />
                </button>
            </div>

            <div className="w-px h-8 bg-border/60 mx-1"></div>

            {/* Colors */}
            <div className="flex gap-2.5 px-2 items-center">
                {colors.map((c) => (
                    <button 
                        key={c}
                        onClick={() => { setColor(c); setTool(tool === 'eraser' ? 'pen' : tool); }}
                        className={`w-6 h-6 rounded-full transition-all relative ${color === c && tool !== 'eraser' ? 'scale-125 shadow-soft z-10' : 'hover:scale-110'}`}
                        style={{ backgroundColor: c }}
                    >
                        {color === c && tool !== 'eraser' && (
                            <span className="absolute -inset-1 rounded-full border-2" style={{ borderColor: c, opacity: 0.5 }}></span>
                        )}
                    </button>
                ))}
            </div>

            <div className="w-px h-8 bg-border/60 mx-1"></div>

            {/* Sizes */}
            <div className="flex gap-3 px-2 items-center justify-center">
                {linePicks.map((s) => (
                    <button 
                        key={s}
                        onClick={() => setLineWidth(s)}
                        className={`bg-text-secondary rounded-full transition-all ${lineWidth === s ? 'bg-primary' : 'hover:bg-text-main'}`}
                        style={{ width: `${s + 4}px`, height: `${s + 4}px` }}
                    />
                ))}
            </div>

            <div className="w-px h-8 bg-border/60 mx-1"></div>

            {/* Actions */}
            <div className="flex items-center gap-1">
                <button onClick={clearCanvas} className="p-2.5 rounded-full text-text-muted hover:text-primary transition-colors" title="Clear Canvas">
                    <Sparkles size={18} />
                </button>
                <button onClick={exportCanvas} className="flex items-center gap-2 bg-surface px-4 py-2 rounded-full border border-border/50 text-sm font-bold text-text-main hover:text-primary transition-colors shadow-sm ml-1" title="Export Image">
                    <Download size={16} />
                    <span className="hidden sm:inline">Export</span>
                </button>
            </div>
        </div>

        {/* Paper Textured Canvas Workspace */}
        <main className="flex-1 w-full h-full relative bg-white m-4 md:m-6 rounded-[2.5rem] shadow-sm border border-border/40 overflow-hidden group">
            
            {/* Dot Pattern Background */}
            <div className="absolute inset-0 pointer-events-none opacity-30" 
                 style={{ backgroundImage: 'radial-gradient(circle, #9ca3af 1.5px, transparent 1.5px)', backgroundSize: '24px 24px' }}>
            </div>

            {/* Placeholder Empty State (Visible only if not drawn) */}
            {!hasDrawn && (
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none z-10 transition-opacity duration-300">
                    <div className="w-20 h-20 bg-primary/10 rounded-[1.5rem] flex items-center justify-center text-primary mb-6 shadow-sm">
                        <PenTool size={32} strokeWidth={2.5} />
                    </div>
                    <h2 className="text-3xl font-bold text-text-main tracking-tight">Premium Workspace</h2>
                    <p className="text-text-secondary mt-3 max-w-sm text-center leading-relaxed">
                        Capture your best ideas on our tactile paper-textured digital canvas.
                    </p>
                </div>
            )}

            {/* The Actual Canvas Component */}
            <canvas
                ref={canvasRef}
                className="absolute inset-0 touch-none w-full h-full cursor-crosshair z-20"
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={endDrawing}
                onMouseOut={endDrawing}
                onTouchStart={startDrawing}
                onTouchMove={draw}
                onTouchEnd={endDrawing}
            />

            {/* Bottom Actions Floating Overlay */}
            <div className="absolute bottom-6 left-6 z-30 flex flex-col gap-3">
                <button onClick={handleUndo} className="p-3 bg-surface rounded-2xl shadow-card border border-border/50 text-text-secondary hover:text-primary transition-colors" title="Undo">
                    <Undo2 size={20} />
                </button>
                <button onClick={handleRedo} className="p-3 bg-surface rounded-2xl shadow-card border border-border/50 text-text-secondary hover:text-primary transition-colors" title="Redo">
                    <Redo2 size={20} />
                </button>
                <button className="p-3 bg-surface rounded-2xl shadow-card border border-border/50 text-text-secondary hover:text-primary transition-colors mt-2" title="Zoom In">
                    <ZoomIn size={20} />
                </button>
            </div>

            {/* Bottom Status Tickers */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-30 flex items-center gap-6 md:gap-10 opacity-60 pointer-events-none display-none sm:flex">
                <div className="flex items-center gap-2">
                    <div className="w-1.5 h-3 bg-primary rounded-full"></div>
                    <span className="text-[10px] font-bold text-text-main tracking-widest leading-tight uppercase">Canvas<br/>Synced</span>
                </div>
                <div className="w-px h-6 bg-border"></div>
                <div className="text-[10px] font-bold text-text-secondary tracking-widest leading-tight uppercase">4K<br/>Resolution</div>
                <div className="w-px h-6 bg-border"></div>
                <div className="text-[10px] font-bold text-text-secondary tracking-widest leading-tight uppercase">Pressure<br/>Enabled</div>
            </div>

        </main>
      </div>

      {/* Right Custom Gallery Panel specific to Drawing Pad */}
      <aside className="hidden xl:flex fixed inset-y-0 right-0 w-[340px] bg-[#f8fafc] border-l border-border/50 flex-col py-8 px-6 shadow-[-10px_0_30px_rgba(0,0,0,0.02)] z-40">
        
        {/* Gallery Header */}
        <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-3">
                <ImageIcon className="text-primary" size={24} />
                <h2 className="text-xl font-bold text-text-main">Gallery</h2>
            </div>
            <span className="bg-primary/10 text-primary text-[10px] font-bold px-3 py-1.5 rounded-full tracking-wider">
                12 SKETCHES
            </span>
        </div>

        {/* Sketch Cards Container */}
        <div className="flex-1 flex flex-col gap-5 overflow-y-auto custom-scrollbar pr-2 pb-6">
            
            {/* Simulated Card 1 */}
            <div className="group cursor-pointer">
                <div className="bg-white rounded-[1.5rem] border border-border/60 p-2 shadow-sm group-hover:shadow-card transition-all mb-3 h-40 flex items-center justify-center overflow-hidden">
                    <div className="w-24 h-24 rounded-full border-4 border-[#8B7355] flex items-center justify-center opacity-70">
                         <div className="w-20 h-20 rounded-full border border-dashed border-[#8B7355]"></div>
                    </div>
                </div>
                <div className="flex justify-between items-start px-1">
                    <div>
                        <h4 className="text-sm font-bold text-text-main group-hover:text-primary transition-colors">Molecular Structure</h4>
                        <p className="text-xs text-text-muted mt-0.5">Oct 24, 2023</p>
                    </div>
                    <button className="text-text-muted hover:text-text-main"><MoreVertical size={16} /></button>
                </div>
            </div>

            {/* Simulated Card 2 */}
            <div className="group cursor-pointer">
                <div className="bg-white rounded-[1.5rem] border border-border/60 p-2 shadow-sm group-hover:shadow-card transition-all mb-3 h-40 flex items-center justify-center overflow-hidden">
                    <div className="w-16 flex gap-2 rotate-45 opacity-60">
                         <div className="w-4 h-24 bg-[#4A5568] rounded-full"></div>
                         <div className="w-8 h-24 bg-[#4A5568] rounded-full"></div>
                         <div className="w-4 h-24 bg-[#4A5568] rounded-full"></div>
                    </div>
                </div>
                <div className="flex justify-between items-start px-1">
                    <div>
                        <h4 className="text-sm font-bold text-text-main group-hover:text-primary transition-colors">Flowchart Draft</h4>
                        <p className="text-xs text-text-muted mt-0.5">Oct 22, 2023</p>
                    </div>
                    <button className="text-text-muted hover:text-text-main"><MoreVertical size={16} /></button>
                </div>
            </div>

            {/* Simulated Card 3 (Empty) */}
            <div className="group cursor-pointer">
                <div className="bg-white rounded-[1.5rem] border border-border/60 p-2 shadow-sm group-hover:shadow-card transition-all mb-3 h-40 flex items-center justify-center bg-[#f1f5f9]/50">
                    <ImageIcon className="text-text-muted/30" size={32} />
                </div>
                <div className="flex justify-between items-start px-1">
                    <div>
                        <h4 className="text-sm font-bold text-text-main group-hover:text-primary transition-colors">Mind Map V2</h4>
                        <p className="text-xs text-text-muted mt-0.5">Oct 19, 2023</p>
                    </div>
                    <button className="text-text-muted hover:text-text-main"><MoreVertical size={16} /></button>
                </div>
            </div>

        </div>

        {/* Bottom Button */}
        <div className="pt-4 border-t border-border/50 shrink-0">
            <button className="w-full py-3.5 bg-surface border border-border/80 shadow-sm rounded-2xl flex items-center justify-center gap-2 text-sm font-bold text-text-secondary hover:text-primary hover:border-primary/30 transition-all group">
                <Cloud size={18} className="group-hover:-translate-y-0.5 transition-transform" />
                Sync Cloud Gallery
            </button>
        </div>
      </aside>

    </div>
  );
};

export default DrawingPad;
