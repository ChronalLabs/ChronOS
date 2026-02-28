import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import RightPanel from "../components/RightPanel";
import { useAuth } from "../context/AuthContext";
import {
  Bold,
  Italic,
  List,
  ImageIcon,
  Link2,
  Share2,
  ChevronRight,
  Plus,
  CheckCircle2,
  Circle,
  Sparkles,
  Menu,
  BookOpen,
} from "lucide-react";
import { motion } from "framer-motion";

/* ─── mock library ────────────────── */
const LIBRARY = [
  {
    name: "Physics III",
    open: true,
    children: ["Quantum Mechanics", "Electromagnetism", "Thermodynamics"],
    active: "Electromagnetism",
  },
  { name: "Calc Advanced", open: false, children: [] },
  { name: "World History", open: false, children: [] },
];

/* ─── mock tasks ────────────────── */
const TASKS = [
  { text: "Solve Ch 4 Practice Problems", due: "Due tomorrow", done: false },
  { text: "Read introduction section", due: "Completed", done: true },
];

/* ═══════════════════════════════════════════════════════════════ */

const Notepad = () => {
  const { user } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [library, setLibrary] = useState(LIBRARY);
  const [title, setTitle] = useState("Electromagnetism Notes");
  const [tasks, setTasks] = useState(TASKS);

  const toggleFolder = (idx) => {
    setLibrary((prev) =>
      prev.map((item, i) => (i === idx ? { ...item, open: !item.open } : item)),
    );
  };

  const toggleTask = (idx) => {
    setTasks((prev) =>
      prev.map((t, i) => (i === idx ? { ...t, done: !t.done } : t)),
    );
  };

  return (
    <div className="min-h-screen bg-background flex font-sans text-text-main relative overflow-hidden">
      {/* mobile overlay */}
      {isSidebarOpen && (
        <div
          onClick={() => setIsSidebarOpen(false)}
          className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm"
        />
      )}

      {/* sidebar (app‑wide) */}
      <div
        className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
      </div>

      {/* right panel (app‑wide) */}
      <div className="hidden xl:block fixed inset-y-0 right-0 z-50">
        <RightPanel />
      </div>

      {/* ─── main area ─── */}
      <div className="flex-1 md:ml-20 xl:mr-80 main-content right-panel-transition flex h-screen overflow-hidden">
        {/* ─── library sidebar (local) ─── */}
        <aside className="hidden lg:flex w-64 border-r border-border bg-surface/50 flex-col shrink-0 overflow-y-auto">
          <div className="p-6">
            <h2 className="text-xs font-bold uppercase tracking-widest text-text-muted mb-4 px-2">
              Library
            </h2>

            <div className="space-y-1">
              {library.map((folder, fi) => (
                <div key={fi}>
                  <button
                    onClick={() => toggleFolder(fi)}
                    className={`w-full flex items-center justify-between p-2 rounded-xl transition-all ${
                      folder.open
                        ? "bg-primary/10 text-primary font-medium"
                        : "text-text-secondary hover:bg-surface-hover"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <BookOpen size={18} />
                      <span className="text-sm">{folder.name}</span>
                    </div>
                    <ChevronRight
                      size={14}
                      className={`transition-transform ${folder.open ? "rotate-90" : ""}`}
                    />
                  </button>

                  {folder.open && folder.children.length > 0 && (
                    <div className="ml-4 pl-4 border-l-2 border-border space-y-1 mt-1">
                      {folder.children.map((child) => (
                        <button
                          key={child}
                          className={`w-full text-left p-2 text-sm rounded-lg transition-colors ${
                            folder.active === child
                              ? "text-primary font-medium bg-primary/5"
                              : "text-text-secondary hover:bg-surface-hover"
                          }`}
                        >
                          {child}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            <button className="mt-8 w-full flex items-center gap-2 p-2 text-sm text-text-muted hover:text-primary border-2 border-dashed border-border rounded-xl transition-all hover:border-primary">
              <Plus size={16} />
              <span>New Notebook</span>
            </button>
          </div>
        </aside>

        {/* ─── editor area ─── */}
        <main className="flex-1 flex flex-col bg-surface overflow-hidden">
          {/* toolbar */}
          <header className="h-14 border-b border-border flex items-center justify-between px-4 md:px-6 bg-surface/80 backdrop-blur-md sticky top-0 z-10 shrink-0">
            {/* mobile menu */}
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="md:hidden p-2 text-text-secondary hover:text-primary"
            >
              <Menu size={22} />
            </button>

            {/* breadcrumb */}
            <div className="hidden md:flex items-center gap-2 text-sm text-text-muted">
              <span>Physics III</span>
              <ChevronRight size={14} />
              <span className="text-text-main font-medium">
                Electromagnetism
              </span>
            </div>

            {/* format buttons */}
            <div className="flex items-center gap-1 border-x border-border px-3">
              {[Bold, Italic, List, ImageIcon, Link2].map((Icon, i) => (
                <button
                  key={i}
                  className="p-2 text-text-muted hover:bg-surface-hover hover:text-text-main rounded-lg transition-colors"
                >
                  <Icon size={18} />
                </button>
              ))}
            </div>

            <div className="flex items-center gap-3">
              <span className="text-xs text-text-muted italic hidden sm:inline">
                Saved 2m ago
              </span>
              <button className="btn-primary flex items-center gap-2 !px-4 !py-2 text-sm">
                <Share2 size={16} /> Share
              </button>
            </div>
          </header>

          {/* content */}
          <div className="flex-1 overflow-y-auto px-6 py-10 md:px-16 lg:px-24">
            <div className="max-w-3xl mx-auto">
              {/* title input */}
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full text-3xl md:text-4xl font-bold border-none bg-transparent focus:ring-0 text-text-main mb-8 p-0 placeholder:text-text-muted outline-none"
                placeholder="Untitled Document"
              />

              {/* body text */}
              <div className="space-y-6 text-lg leading-relaxed text-text-secondary">
                <p>
                  Electromagnetism is a branch of physics involving the study of
                  the electromagnetic force, a type of physical interaction that
                  occurs between electrically charged particles. The
                  electromagnetic force is carried by electromagnetic fields
                  composed of electric fields and magnetic fields, and it is
                  responsible for electromagnetic radiation such as light.
                </p>

                {/* Maxwell heading */}
                <h3 className="text-2xl font-bold text-text-main flex items-center gap-2 mt-10 mb-4">
                  <span className="w-1 h-6 bg-primary rounded-full" />
                  Maxwell's Equations
                </h3>

                {/* formula card */}
                <div className="bg-background p-6 rounded-2xl border border-border space-y-4">
                  <p className="font-mono text-sm text-primary italic">
                    // Important Formulas for Midterm
                  </p>
                  <div className="flex items-center gap-4">
                    <span className="bg-surface px-3 py-1 rounded-lg text-text-main border border-border font-mono text-sm">
                      ∇ · E = ρ / ε₀
                    </span>
                    <span className="text-xs text-text-muted">Gauss's Law</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className="bg-surface px-3 py-1 rounded-lg text-text-main border border-border font-mono text-sm">
                      ∇ · B = 0
                    </span>
                    <span className="text-xs text-text-muted">
                      Gauss's Law for Magnetism
                    </span>
                  </div>
                </div>

                <p>
                  In the classical limit, the electric field is produced by
                  stationary charges, and the magnetic field is produced by
                  moving charges (electric currents). These two are actually
                  different aspects of the same phenomenon, which is why we
                  refer to it as electromagnetism.
                </p>

                {/* drop zone */}
                <div className="mt-12 flex items-center justify-center p-12 border-2 border-dashed border-border rounded-3xl group cursor-pointer hover:bg-surface-hover transition-all">
                  <div className="text-center">
                    <Plus
                      size={40}
                      className="mx-auto text-text-muted group-hover:text-primary transition-colors mb-2"
                    />
                    <p className="text-sm text-text-muted group-hover:text-text-secondary transition-colors">
                      Click or drag to add images, videos, or diagrams
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>

        {/* ─── document info sidebar (local) ─── */}
        <aside className="hidden lg:flex w-80 border-l border-border bg-background/50 flex-col shrink-0 overflow-y-auto p-6 gap-6">
          {/* document info */}
          <div>
            <h3 className="text-sm font-bold text-text-main mb-4 flex items-center gap-2">
              <span className="text-primary">ℹ</span> Document Info
            </h3>
            <div className="bg-surface p-4 rounded-2xl shadow-card border border-border/50 space-y-4">
              {[
                ["Word Count", "142 words"],
                ["Read Time", "1 min"],
                ["Created", "Oct 12, 2023"],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between items-center">
                  <span className="text-xs text-text-muted">{label}</span>
                  <span className="text-xs font-medium text-text-secondary">
                    {value}
                  </span>
                </div>
              ))}
              <div className="pt-2 border-t border-border/50">
                <span className="text-xs text-text-muted block mb-2">Tags</span>
                <div className="flex flex-wrap gap-2">
                  {[
                    {
                      label: "Physics",
                      bg: "bg-primary-light",
                      color: "text-primary",
                    },
                    {
                      label: "Midterm",
                      bg: "bg-blue-100",
                      color: "text-blue-500",
                    },
                    {
                      label: "Notes",
                      bg: "bg-purple-100",
                      color: "text-purple-500",
                    },
                  ].map((tag) => (
                    <span
                      key={tag.label}
                      className={`${tag.bg} ${tag.color} text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-wider`}
                    >
                      {tag.label}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* related tasks */}
          <div>
            <h3 className="text-sm font-bold text-text-main mb-4 flex items-center gap-2">
              <span className="text-primary">📋</span> Related Tasks
            </h3>
            <div className="space-y-3">
              {tasks.map((task, idx) => (
                <div
                  key={idx}
                  onClick={() => toggleTask(idx)}
                  className="flex items-start gap-3 p-3 bg-surface rounded-xl border border-border/50 cursor-pointer hover:shadow-soft transition-all"
                >
                  {task.done ? (
                    <CheckCircle2
                      size={18}
                      className="mt-0.5 text-primary shrink-0"
                    />
                  ) : (
                    <Circle
                      size={18}
                      className="mt-0.5 text-text-muted shrink-0"
                    />
                  )}
                  <div className="flex-1">
                    <p
                      className={`text-xs font-medium ${task.done ? "text-text-muted line-through" : "text-text-main"}`}
                    >
                      {task.text}
                    </p>
                    <p className="text-[10px] text-text-muted mt-1">
                      {task.due}
                    </p>
                  </div>
                </div>
              ))}
              <button className="w-full py-3 flex items-center justify-center gap-2 text-xs font-medium text-primary hover:bg-primary/5 rounded-xl border border-dashed border-primary/30 transition-all">
                <Plus size={14} /> Link another task
              </button>
            </div>
          </div>

          {/* AI insight */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-auto p-4 bg-gradient-to-br from-primary-light to-surface rounded-2xl border border-primary/10"
          >
            <div className="flex items-center gap-2 mb-3">
              <Sparkles size={16} className="text-primary" />
              <span className="text-xs font-bold text-text-main">
                AI Study Insights
              </span>
            </div>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Based on your notes, you might want to review{" "}
              <span className="text-primary font-medium">Faraday's Law</span>{" "}
              next. There's a high probability it will be on the midterm.
            </p>
            <button className="mt-3 w-full text-[11px] font-bold text-white bg-primary py-2 rounded-lg hover:bg-primary-dark transition-colors">
              Generate Summary
            </button>
          </motion.div>
        </aside>
      </div>
    </div>
  );
};

export default Notepad;
