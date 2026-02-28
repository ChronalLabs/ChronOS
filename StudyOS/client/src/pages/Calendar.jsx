import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import RightPanel from "../components/RightPanel";
import { ChevronLeft, ChevronRight, Menu, Filter, Search, Bell } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const CalendarPage = () => {
  const { user } = useAuth();
  const [view, setView] = useState("Month");
  const [searchQuery, setSearchQuery] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Month mock days (starting from 28th of previous to show standard calendar UI)
  const days = [
    { num: 28, isCurrentMonth: false, events: [] },
    { num: 29, isCurrentMonth: false, events: [] },
    { num: 30, isCurrentMonth: false, events: [] },
    { num: 31, isCurrentMonth: false, events: [] },
    { num: 1, isCurrentMonth: true, events: [] },
    { num: 2, isCurrentMonth: true, events: [{ title: 'Math Quiz', color: 'bg-blue-100 text-blue-600' }] },
    { num: 3, isCurrentMonth: true, events: [] },

    { num: 4, isCurrentMonth: true, events: [] },
    { num: 5, isCurrentMonth: true, events: [
        { title: 'Physics Prep', color: 'bg-green-100 text-green-700' },
        { title: 'History Lab', color: 'bg-yellow-100 text-yellow-700' }
    ] },
    { num: 6, isCurrentMonth: true, active: true, events: [{ title: 'Chemistry Exam', color: 'bg-primary text-white' }] },
    { num: 7, isCurrentMonth: true, events: [] },
    { num: 8, isCurrentMonth: true, events: [] },
    { num: 9, isCurrentMonth: true, events: [] },
    { num: 10, isCurrentMonth: true, events: [] },

    { num: 11, isCurrentMonth: true, events: [] },
    { num: 12, isCurrentMonth: true, events: [{ title: 'Coding Sprint', color: 'bg-purple-100 text-purple-700' }] },
    { num: 13, isCurrentMonth: true, events: [] },
    { num: 14, isCurrentMonth: true, events: [] },
    { num: 15, isCurrentMonth: true, events: [] },
    { num: 16, isCurrentMonth: true, events: [] },
    { num: 17, isCurrentMonth: true, events: [] },

    { num: 18, isCurrentMonth: true, events: [{ title: 'Gym Session', color: 'bg-pink-100 text-pink-700' }] },
    { num: 19, isCurrentMonth: true, events: [] },
    { num: 20, isCurrentMonth: true, events: [] },
    { num: 21, isCurrentMonth: true, events: [] },
    { num: 22, isCurrentMonth: true, events: [] },
    { num: 23, isCurrentMonth: true, events: [] },
    { num: 24, isCurrentMonth: true, events: [] },

    { num: 25, isCurrentMonth: true, events: [] },
    { num: 26, isCurrentMonth: true, events: [] },
    { num: 27, isCurrentMonth: true, events: [] },
    { num: 28, isCurrentMonth: true, events: [] },
    { num: 29, isCurrentMonth: true, events: [] },
    { num: 30, isCurrentMonth: true, events: [] },
    { num: 1, isCurrentMonth: false, events: [] }, // padded end
  ];

  return (
    <div className="flex bg-background min-h-screen text-text-main font-sans overflow-hidden">
      {/* 1) Optional Mobile Overlay */}
      {isSidebarOpen && (
        <div
          onClick={() => setIsSidebarOpen(false)}
          className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm"
        />
      )}

      {/* 2) Left Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 transform transition-transform duration-300 ease-in-out md:translate-x-0 ${
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <Sidebar onMobileClose={() => setIsSidebarOpen(false)} />
      </div>

      {/* 3) Main Content Area Wrapper */}
      <div className="flex-1 flex flex-col md:ml-20 xl:mr-80 min-h-screen relative transition-all duration-300 z-10">
        
        {/* Main Content */}
        <main className="flex-1 p-4 md:p-8 overflow-y-auto w-full max-w-7xl mx-auto space-y-8">
            {/* Header section similar to Notes/Sticky Notes */}
            <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
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

              <div className="relative w-full md:w-96 group z-20">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-primary transition-colors" size={20} />
                <input
                  type="text"
                  placeholder="Search tasks, notes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3.5 bg-surface border border-transparent focus:bg-surface focus:border-primary/20 focus:ring-4 focus:ring-primary/5 rounded-2xl text-text-main shadow-card hover:shadow-soft transition-all outline-none placeholder:text-text-muted"
                />
              </div>

              <div className="hidden md:flex items-center gap-8 z-20">
                <button className="relative p-3 bg-surface rounded-xl text-text-secondary hover:text-primary hover:shadow-soft transition-all duration-200 border border-transparent hover:border-border/50">
                  <Bell size={22} />
                  <span className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border-2 border-surface" />
                </button>
                <div className="flex items-center gap-4 pl-8 border-l border-border/60">
                  <div className="text-right hidden lg:block">
                    <p className="text-sm font-bold text-text-main tracking-tight">
                      {user?.username || 'Arin'}
                    </p>
                    <p className="text-xs text-text-secondary font-medium">Level 1 Scholar</p>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center text-primary font-bold text-lg shadow-inner cursor-pointer hover:scale-105 transition-transform">
                    {user?.username ? user.username[0].toUpperCase() : 'A'}
                  </div>
                </div>
              </div>
            </header>

            {/* Calendar View Container */}
            <div className="bg-surface rounded-3xl p-6 md:p-8 shadow-card border border-border/50 w-full mb-8">
                
                {/* Calendar Toolbar */}
                <div className="flex flex-col md:flex-row items-center justify-between gap-4 mb-8">
                    <div className="flex items-center gap-4">
                        <h1 className="text-2xl font-bold text-text-main">September 2024</h1>
                        <div className="flex items-center gap-1 bg-background p-1 rounded-xl shadow-inner border border-transparent text-text-secondary">
                            <button className="p-1.5 rounded-lg hover:bg-surface hover:text-primary hover:shadow-sm transition-all">
                                <ChevronLeft size={20} />
                            </button>
                            <button className="p-1.5 rounded-lg hover:bg-surface hover:text-primary hover:shadow-sm transition-all">
                                <ChevronRight size={20} />
                            </button>
                        </div>
                    </div>

                    {/* View Switcher */}
                    <div className="flex bg-background p-1.5 rounded-xl shadow-inner border border-border/20">
                        {["Month", "Week", "Day"].map((v) => (
                            <button
                                key={v}
                                onClick={() => setView(v)}
                                className={`px-6 py-2 rounded-lg text-sm font-semibold transition-all duration-300 ${
                                    view === v
                                        ? "bg-surface text-primary shadow-soft"
                                        : "text-text-secondary hover:text-text-main"
                                }`}
                            >
                                {v}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Grid Header (Days of Week) */}
                <div className="grid grid-cols-7 mb-4">
                    {["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"].map((day) => (
                        <div key={day} className="text-center text-xs font-bold text-text-muted tracking-widest uppercase pb-2">
                            {day}
                        </div>
                    ))}
                </div>

                {/* Calendar Grid */}
                <div className="grid grid-cols-7 bg-border/30 gap-[1px] rounded-2xl overflow-hidden border border-border/50">
                    {days.map((day, idx) => {
                        const isCurrent = day.isCurrentMonth;
                        const isToday = day.active;
                        
                        return (
                            <div 
                                key={idx} 
                                className={`min-h-[120px] lg:min-h-[140px] p-2 md:p-3 relative bg-surface hover:bg-background/40 transition-colors
                                ${!isCurrent ? 'bg-background/30 opacity-70' : ''}
                                `}
                            >
                                <div className="flex justify-between items-start mb-2">
                                    <span className={`w-8 h-8 flex items-center justify-center rounded-full text-sm font-bold
                                        ${isToday ? 'bg-primary text-white shadow-md' : (isCurrent ? 'text-text-main' : 'text-text-muted')}
                                    `}>
                                        {day.num}
                                    </span>
                                </div>
                                
                                <div className="space-y-1.5 mt-2">
                                    {day.events.map((event, eventIdx) => (
                                        <div 
                                            key={eventIdx} 
                                            className={`px-2 py-1.5 text-xs font-bold rounded-lg truncate shadow-sm transition-transform hover:scale-[1.02] cursor-pointer ${event.color}`}
                                        >
                                            {event.title}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>

            </div>
        </main>
      </div>

      {/* 4) Fixed Right Panel (Desktop) */}
      <div className="hidden xl:block fixed inset-y-0 right-0 z-40 w-80">
        <RightPanel />
      </div>

    </div>
  );
};

export default CalendarPage;
