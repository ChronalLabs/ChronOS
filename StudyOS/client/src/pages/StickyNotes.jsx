import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import RightPanel from "../components/RightPanel";
import { useAuth } from "../context/AuthContext";
import {
  Search,
  Bell,
  Plus,
  MoreHorizontal,
  CheckCircle2,
  Circle,
  Menu,
  Filter,
  Pin,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

/* ───────── sample data ───────── */
const CATEGORIES = ["All", "Work", "Study", "Personal"];

const INITIAL_NOTES = [
  {
    id: 1,
    category: "Study",
    label: "Study Prep",
    title: "Physics Exam Revision",
    type: "checklist",
    items: [
      { text: "Review Chapter 4 notes", done: true },
      { text: "Complete practice set A", done: true },
      { text: "Derive Maxwell equations", done: false },
      { text: "Lab report submission", done: false },
    ],
    time: "Modified 2h ago",
    color: "emerald",
  },
  {
    id: 2,
    category: "Work",
    label: "Work",
    title: "Design System Audit",
    type: "bullets",
    items: [
      "Check accessibility contrast for the mint green primary color",
      "Update icon set to Material Round",
      "Verify dark mode border tokens",
    ],
    time: "Modified 3d ago",
    color: "purple",
  },
  {
    id: 3,
    category: "Personal",
    label: "Quick Thought",
    title: "Project Idea: Focus API",
    type: "text",
    body: "Build a lightweight Chrome extension that syncs study sessions directly with the ChronOS dashboard. Should include a simple pomodoro timer and site blocker.",
    time: "Modified 5h ago",
    color: "amber",
  },
  {
    id: 4,
    category: "Study",
    label: "Motivation",
    title: null,
    type: "quote",
    body: '"Success is not final, failure is not fatal: it is the courage to continue that counts."',
    author: "— Winston Churchill",
    time: "Pinned",
    pinned: true,
    color: "emerald",
  },
  {
    id: 5,
    category: "Personal",
    label: "Personal",
    title: "Weekend Reading",
    type: "text",
    body: '"Deep Work" by Cal Newport – focus on the chapters about rhythmic scheduling of deep work sessions.',
    avatars: ["JD", "AK"],
    time: "Modified 1d ago",
    color: "blue",
  },
  {
    id: 6,
    category: "Personal",
    label: "Shopping",
    title: "Desk Setup Upgrade",
    type: "checklist",
    items: [
      { text: "Mechanical Keyboard (Blue switches)", done: false },
      { text: "Large felt desk mat", done: false },
      { text: "Monitor light bar", done: false },
    ],
    time: "Modified 1w ago",
    color: "rose",
  },
];

/* ───── colour map ───── */
const palette = {
  emerald: {
    card: "bg-emerald-50",
    border: "border-emerald-100",
    label: "text-emerald-600",
    title: "text-emerald-900",
    text: "text-emerald-800",
    check: "text-primary",
    uncheck: "text-emerald-300",
    meta: "text-emerald-600",
    dot: "bg-emerald-400",
  },
  purple: {
    card: "bg-purple-50",
    border: "border-purple-100",
    label: "text-purple-600",
    title: "text-purple-900",
    text: "text-purple-800",
    check: "text-primary",
    uncheck: "text-purple-300",
    meta: "text-purple-600",
    dot: "bg-purple-400",
  },
  amber: {
    card: "bg-amber-50",
    border: "border-amber-100",
    label: "text-amber-700",
    title: "text-amber-900",
    text: "text-amber-800",
    check: "text-primary",
    uncheck: "text-amber-300",
    meta: "text-amber-600",
    dot: "bg-amber-400",
  },
  blue: {
    card: "bg-blue-50",
    border: "border-blue-100",
    label: "text-blue-600",
    title: "text-blue-900",
    text: "text-blue-800",
    check: "text-primary",
    uncheck: "text-blue-300",
    meta: "text-blue-600",
    dot: "bg-blue-400",
  },
  rose: {
    card: "bg-rose-50",
    border: "border-rose-100",
    label: "text-rose-600",
    title: "text-rose-900",
    text: "text-rose-800",
    check: "text-primary",
    uncheck: "text-rose-300",
    meta: "text-rose-600",
    dot: "bg-rose-400",
  },
};

/* ═══════════════════════════════════════════════════════════════ */

const StickyNotes = () => {
  const { user } = useAuth();
  const [activeCategory, setActiveCategory] = useState("All");
  const [notes, setNotes] = useState(INITIAL_NOTES);
  const [searchQuery, setSearchQuery] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  /* filter */
  const filtered = notes.filter((n) => {
    const matchCat = activeCategory === "All" || n.category === activeCategory;
    const matchSearch =
      !searchQuery ||
      n.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      n.body?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchCat && matchSearch;
  });

  /* toggle checklist item */
  const toggleItem = (noteId, idx) => {
    setNotes((prev) =>
      prev.map((n) => {
        if (n.id !== noteId || n.type !== "checklist") return n;
        const items = [...n.items];
        items[idx] = { ...items[idx], done: !items[idx].done };
        return { ...n, items };
      }),
    );
  };

  /* ─── render card body ───────────────────────────── */
  const renderBody = (note) => {
    const c = palette[note.color] || palette.emerald;

    if (note.type === "checklist") {
      return (
        <ul className="space-y-3">
          {note.items.map((item, idx) => (
            <li
              key={idx}
              className={`flex items-center gap-3 cursor-pointer ${c.text}`}
              onClick={() => toggleItem(note.id, idx)}
            >
              {item.done ? (
                <CheckCircle2 size={20} className={c.check} />
              ) : (
                <Circle size={20} className={c.uncheck} />
              )}
              <span className={item.done ? "line-through opacity-60" : ""}>
                {item.text}
              </span>
            </li>
          ))}
        </ul>
      );
    }

    if (note.type === "bullets") {
      return (
        <ul className="space-y-2">
          {note.items.map((item, idx) => (
            <li key={idx} className={`flex items-start gap-2 ${c.text}`}>
              <span
                className={`mt-1.5 w-1.5 h-1.5 rounded-full ${c.dot} shrink-0`}
              />
              <span>{item}</span>
            </li>
          ))}
        </ul>
      );
    }

    if (note.type === "quote") {
      return (
        <>
          <p
            className={`${c.title} text-xl font-medium leading-relaxed italic`}
          >
            {note.body}
          </p>
          {note.author && <p className={`mt-4 ${c.text}`}>{note.author}</p>}
        </>
      );
    }

    /* text */
    return (
      <>
        <p
          className={`${c.text} leading-relaxed ${note.type === "text" && !note.title ? "italic" : ""}`}
        >
          {note.body}
        </p>
        {note.avatars && (
          <div className="mt-4 flex -space-x-2">
            {note.avatars.map((a) => (
              <div
                key={a}
                className={`w-8 h-8 rounded-full border-2 border-blue-50 bg-blue-400 flex items-center justify-center text-[10px] text-white font-bold`}
              >
                {a}
              </div>
            ))}
          </div>
        )}
      </>
    );
  };

  /* ─── component ────────────────────────────── */
  return (
    <div className="min-h-screen bg-background flex font-sans text-text-main relative overflow-hidden">
      {/* mobile overlay */}
      {isSidebarOpen && (
        <div
          onClick={() => setIsSidebarOpen(false)}
          className="fixed inset-0 bg-black/60 z-40 md:hidden backdrop-blur-sm"
        />
      )}

      {/* sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
      </div>

      {/* right panel */}
      <div className="hidden xl:block fixed inset-y-0 right-0 z-50">
        <RightPanel />
      </div>

      {/* main content */}
      <main className="flex-1 md:ml-20 xl:mr-80 main-content right-panel-transition p-4 md:p-8 overflow-y-auto h-screen relative z-0">
        {/* ── header ── */}
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          {/* mobile top bar */}
          <div className="flex items-center justify-between w-full md:hidden mb-4">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50"
            >
              <Menu size={24} />
            </button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary/20 rounded-lg flex items-center justify-center text-primary font-bold">
                S
              </div>
              <span className="font-bold text-lg text-text-main">StudyOS</span>
            </div>
            <button className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50">
              <Filter size={24} />
            </button>
          </div>

          {/* search */}
          <div className="relative w-full md:w-96 group">
            <Search
              className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors"
              size={20}
            />
            <input
              type="text"
              placeholder="Search tasks, notes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3.5 bg-surface border border-transparent focus:bg-surface focus:border-primary/20 focus:ring-4 focus:ring-primary/5 rounded-2xl text-text-main shadow-card hover:shadow-soft transition-all outline-none placeholder:text-text-muted"
            />
          </div>

          {/* right controls */}
          <div className="hidden md:flex items-center gap-8">
            <button className="relative p-3 bg-surface rounded-xl text-text-secondary hover:text-primary hover:shadow-soft transition-all duration-200 border border-transparent hover:border-border/50">
              <Bell size={22} />
              <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-surface" />
            </button>
            <div className="flex items-center gap-4 pl-8 border-l border-border/60">
              <div className="text-right hidden lg:block">
                <p className="text-sm font-bold text-text-main tracking-tight">
                  {user?.username || "Student"}
                </p>
                <p className="text-xs text-text-secondary font-medium">
                  Level 1 Scholar
                </p>
              </div>
              <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center text-primary font-bold text-lg shadow-inner cursor-pointer hover:scale-105 transition-transform">
                {user?.username ? user.username[0].toUpperCase() : "S"}
              </div>
            </div>
          </div>
        </header>

        {/* ── title row ── */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div className="flex items-center gap-4 flex-wrap">
            <h1 className="text-2xl font-bold">Sticky Notes</h1>

            {/* category pills */}
            <div className="flex bg-background rounded-xl p-1 shadow-inner">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                    activeCategory === cat
                      ? "bg-surface shadow-soft text-text-main"
                      : "text-text-muted hover:text-text-secondary"
                  }`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>

          <button className="btn-primary flex items-center gap-2">
            <Plus size={18} /> New Note
          </button>
        </div>

        {/* ── masonry grid ── */}
        <div className="columns-1 md:columns-2 xl:columns-3 gap-6">
          <AnimatePresence>
            {filtered.map((note) => {
              const c = palette[note.color] || palette.emerald;
              return (
                <motion.div
                  key={note.id}
                  layout
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className={`break-inside-avoid mb-6 group relative ${c.card} p-6 rounded-3xl shadow-card border ${c.border} transition-transform hover:-translate-y-1`}
                >
                  {/* header */}
                  <div className="flex items-center justify-between mb-4">
                    <span
                      className={`text-[10px] font-bold uppercase tracking-wider ${c.label}`}
                    >
                      {note.label}
                    </span>
                    <button
                      className={`opacity-0 group-hover:opacity-100 transition-opacity ${c.label}`}
                    >
                      <MoreHorizontal size={18} />
                    </button>
                  </div>

                  {note.title && (
                    <h3 className={`font-bold text-lg mb-3 ${c.title}`}>
                      {note.title}
                    </h3>
                  )}

                  {renderBody(note)}

                  <p
                    className={`mt-6 text-[11px] font-medium ${c.meta} flex items-center gap-1`}
                  >
                    {note.pinned && <Pin size={12} className="inline" />}
                    {note.time}
                  </p>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20 text-text-muted">
            <p className="text-lg">No notes found.</p>
          </div>
        )}
      </main>

      {/* mobile FAB */}
      <button className="xl:hidden fixed bottom-6 right-6 w-14 h-14 bg-primary text-white rounded-full shadow-glow flex items-center justify-center z-50 hover:scale-105 transition-transform">
        <Plus size={24} />
      </button>
    </div>
  );
};

export default StickyNotes;
