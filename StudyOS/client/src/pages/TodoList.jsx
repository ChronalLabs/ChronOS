import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import RightPanel from "../components/RightPanel";
import { Menu, Plus, MoreHorizontal, Paperclip, MessageSquare, Calendar, Clock, CheckCircle2 } from "lucide-react";

// Mock Data
const initialTasks = {
  todo: [
    {
      id: "t1",
      title: "Research Paper Outline",
      description: "Structure the thesis statement and primary arguments for the upcoming physics...",
      priority: "HIGH PRIORITY",
      priorityColor: "bg-red-100 text-red-600",
      progress: 0,
      avatars: ["JS", "MK"],
      date: "Oct 24",
      attachments: 0,
      comments: 0
    },
    {
      id: "t2",
      title: "Lab Report Drafting",
      description: "",
      priority: "MEDIUM",
      priorityColor: "bg-yellow-100 text-yellow-700",
      progress: 0,
      avatars: ["AL"],
      attachments: 3,
      comments: 12
    }
  ],
  inProgress: [
    {
      id: "p1",
      title: "Algorithm Finalization",
      description: "Optimizing the recursive functions for the data structures project.",
      priority: "URGENT",
      priorityColor: "bg-red-100 text-red-600",
      progress: 65,
      avatars: ["RT"],
      extraAvatars: "+2",
      timeLeft: "2h left",
      attachments: 0,
      comments: 0
    }
  ],
  completed: [
    {
      id: "c1",
      title: "Midterm Preparation",
      description: "",
      priority: "DONE",
      priorityColor: "bg-primary/10 text-primary",
      progress: 100,
      avatars: ["JS"],
      completedStatus: "Completed Yesterday",
      attachments: 0,
      comments: 0
    }
  ]
};

const TaskCard = ({ task, columnId, moveTask }) => {
  return (
    <div className="bg-surface rounded-[1.5rem] p-5 shadow-sm border border-border/50 hover:shadow-card transition-all group relative">
      
      {/* Complete Checkbox for Drag Simulation */}
      {columnId !== 'completed' && (
        <button 
            onClick={() => moveTask(task.id, columnId, 'completed')}
            className="absolute -right-3 -top-3 w-8 h-8 bg-background border border-border rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-primary/10 hover:text-primary shadow-sm z-10"
            title="Mark Complete"
        >
            <CheckCircle2 size={16} />
        </button>
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-3">
        <span className={`text-[10px] font-bold px-2.5 py-1 rounded-md tracking-wider ${task.priorityColor}`}>
          {task.priority}
        </span>
        <button className="text-text-muted hover:text-text-main transition-colors">
          <MoreHorizontal size={18} />
        </button>
      </div>

      {/* Body */}
      <h3 className="font-bold text-text-main text-lg mb-2">{task.title}</h3>
      {task.description && (
        <p className="text-sm text-text-secondary leading-relaxed mb-4 line-clamp-2">
          {task.description}
        </p>
      )}

      {/* Progress Bar */}
      {(task.progress > 0 || columnId === 'todo') && columnId !== 'completed' && (
        <div className="mb-5">
            <div className="flex justify-between text-xs font-semibold text-text-muted mb-1.5">
                <span className="uppercase tracking-wider">Progress</span>
                <span className={task.progress > 0 ? "text-primary" : ""}>{task.progress}%</span>
            </div>
            <div className="w-full h-1.5 bg-background rounded-full overflow-hidden">
                <div 
                    className="h-full bg-primary rounded-full transition-all duration-500" 
                    style={{ width: `${task.progress}%` }}
                />
            </div>
        </div>
      )}
      
      {columnId === 'completed' && (
          <div className="mb-5">
             <div className="w-full h-1.5 bg-primary rounded-full overflow-hidden"></div>
          </div>
      )}

      {/* Footer Metrics */}
      <div className="flex items-center justify-between mt-auto">
        
        {/* Left: Avatars or Attachments */}
        <div className="flex items-center gap-3">
            {task.avatars && (
                <div className="flex -space-x-2">
                    {task.avatars.map((av, i) => (
                        <div key={i} className="w-7 h-7 rounded-full bg-blue-100 flex items-center justify-center text-[10px] font-bold text-blue-700 border-2 border-surface z-10">
                            {av}
                        </div>
                    ))}
                    {task.extraAvatars && (
                        <div className="w-7 h-7 rounded-full bg-background flex items-center justify-center text-[10px] font-bold text-text-secondary border-2 border-surface z-0">
                            {task.extraAvatars}
                        </div>
                    )}
                </div>
            )}
            
            {(!task.avatars && task.attachments > 0) && (
                <div className="flex items-center gap-1.5 text-xs font-medium text-text-muted">
                    <Paperclip size={14} />
                    <span>{task.attachments} Attachments</span>
                </div>
            )}
        </div>

        {/* Right: Dates, Time, or Comments */}
        <div className="flex items-center gap-3">
            {task.date && (
                <div className="flex items-center gap-1.5 text-xs font-semibold text-text-muted">
                    <Calendar size={14} />
                    <span>{task.date}</span>
                </div>
            )}
            {task.timeLeft && (
                <div className="flex items-center gap-1.5 text-xs font-bold text-red-500 bg-red-50 px-2 py-1 rounded-md">
                    <Clock size={14} />
                    <span>{task.timeLeft}</span>
                </div>
            )}
            {task.comments > 0 && (
                <div className="flex items-center gap-1.5 text-xs font-semibold text-text-muted">
                    <MessageSquare size={14} />
                    <span>{task.comments}</span>
                </div>
            )}
            {task.completedStatus && (
                <span className="text-[10px] font-medium text-text-muted">
                    {task.completedStatus}
                </span>
            )}
            {columnId === 'completed' && !task.completedStatus && (
                <CheckCircle2 size={18} className="text-primary" />
            )}
        </div>

      </div>
    </div>
  );
};


const TodoList = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [focusMode, setFocusMode] = useState(false);
  const [tasks, setTasks] = useState(initialTasks);

  // Simple move function to demonstrate interactivity
  const moveTask = (taskId, sourceCol, destCol) => {
    setTasks(prev => {
        const up = { ...prev };
        const taskToMove = up[sourceCol].find(t => t.id === taskId);
        
        if (taskToMove) {
            up[sourceCol] = up[sourceCol].filter(t => t.id !== taskId);
            
            // Adjust properties if moving to completed
            if (destCol === 'completed') {
                taskToMove.progress = 100;
                taskToMove.priority = "DONE";
                taskToMove.priorityColor = "bg-primary/10 text-primary";
                taskToMove.completedStatus = "Just now";
            } else if (destCol === 'inProgress') {
                taskToMove.progress = 50;
            }

            up[destCol] = [taskToMove, ...up[destCol]];
        }
        return up;
    });
  };

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
        <main className="flex-1 p-6 md:p-8 overflow-y-auto w-full mx-auto max-w-[1600px] h-screen flex flex-col">
          
          {/* Header */}
          <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8 shrink-0">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="p-2 bg-surface rounded-xl text-text-secondary hover:text-primary transition-colors border border-border/50 md:hidden"
              >
                <Menu size={24} />
              </button>
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-text-main">Premium Kanban Board</h1>
                <p className="text-sm text-text-secondary mt-1">Manage your study workflow and group projects</p>
              </div>
            </div>
            
            <div className="flex gap-4 items-center w-full md:w-auto overflow-x-auto pb-2 md:pb-0 hide-scrollbar">
                {/* Focus mode toggle */}
                <div className="flex items-center gap-3 bg-surface px-4 py-2 rounded-full border border-border/50 shadow-sm shrink-0">
                    <span className="text-xs font-bold text-text-muted uppercase tracking-widest">Focus Mode</span>
                    <button 
                        onClick={() => setFocusMode(!focusMode)}
                        className={`relative w-10 h-5 rounded-full transition-colors ${focusMode ? 'bg-primary' : 'bg-border'}`}
                    >
                        <span className={`absolute top-1 w-3 h-3 bg-white rounded-full transition-all ${focusMode ? 'left-6' : 'left-1'}`}></span>
                    </button>
                </div>

                <div className="flex items-center gap-2 bg-surface px-4 py-2 rounded-full shadow-sm border border-border/50 shrink-0">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    <span className="text-sm font-medium text-text-secondary">Session: Advanced Calculus</span>
                </div>
            </div>
          </header>

          {/* Kanban Columns */}
          <div className="flex-1 flex gap-6 overflow-x-auto pb-6 custom-scrollbar items-start">
            
            {/* Column 1: To Do */}
            <div className="min-w-[320px] w-[320px] flex-shrink-0 flex flex-col bg-transparent">
                <div className="flex items-center justify-between mb-5 px-1">
                    <div className="flex items-center gap-3">
                        <div className="w-1.5 h-5 bg-border rounded-full"></div>
                        <h2 className="font-bold text-lg text-text-main">To Do</h2>
                        <span className="bg-surface border border-border/50 text-text-secondary text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full shadow-sm">
                            {tasks.todo.length}
                        </span>
                    </div>
                    <button className="text-text-muted hover:text-text-main p-1">
                        <Plus size={18} />
                    </button>
                </div>
                <div className="flex flex-col gap-4">
                    {tasks.todo.map(task => (
                        <TaskCard key={task.id} task={task} columnId="todo" moveTask={moveTask} />
                    ))}
                    {tasks.todo.length === 0 && (
                        <div className="border-2 border-dashed border-border/50 rounded-[1.5rem] h-32 flex items-center justify-center text-text-muted font-medium text-sm">
                            No tasks right now
                        </div>
                    )}
                </div>
            </div>

            {/* Column 2: In Progress */}
            <div className="min-w-[320px] w-[320px] flex-shrink-0 flex flex-col bg-transparent">
                <div className="flex items-center justify-between mb-5 px-1">
                    <div className="flex items-center gap-3">
                        <div className="w-1.5 h-5 bg-primary rounded-full shadow-[0_0_8px_rgba(16,185,129,0.4)]"></div>
                        <h2 className="font-bold text-lg text-text-main">In Progress</h2>
                        <span className="bg-primary/10 text-primary border border-primary/20 text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full">
                            {tasks.inProgress.length}
                        </span>
                    </div>
                    <button className="text-text-muted hover:text-text-main p-1">
                        <Plus size={18} />
                    </button>
                </div>
                <div className="flex flex-col gap-4">
                    {tasks.inProgress.map(task => (
                        <TaskCard key={task.id} task={task} columnId="inProgress" moveTask={moveTask} />
                    ))}
                    {tasks.inProgress.length === 0 && (
                        <div className="border-2 border-dashed border-border/50 rounded-[1.5rem] h-32 flex items-center justify-center text-text-muted font-medium text-sm">
                            Drop tasks here to work
                        </div>
                    )}
                </div>
            </div>

            {/* Column 3: Completed */}
            <div className="min-w-[320px] w-[320px] flex-shrink-0 flex flex-col bg-transparent">
                <div className="flex items-center justify-between mb-5 px-1">
                    <div className="flex items-center gap-3">
                        <div className="w-1.5 h-5 bg-primary rounded-full"></div>
                        <h2 className="font-bold text-lg text-text-main">Completed</h2>
                        <span className="bg-primary/10 text-primary border border-primary/20 text-xs font-bold w-6 h-6 flex items-center justify-center rounded-full">
                            {tasks.completed.length}
                        </span>
                    </div>
                    <button className="text-text-muted hover:text-text-main p-1">
                        <Plus size={18} />
                    </button>
                </div>
                <div className="flex flex-col gap-4 opacity-75 hover:opacity-100 transition-opacity">
                    {tasks.completed.map(task => (
                        <TaskCard key={task.id} task={task} columnId="completed" moveTask={moveTask} />
                    ))}
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

export default TodoList;
