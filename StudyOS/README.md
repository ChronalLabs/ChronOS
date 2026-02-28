# 🎓 StudyOS

**StudyOS** is a premier, study-oriented productivity workspace tailored for students and lifelong learners. It unifies task management, scheduling, and creative tools into a single, cohesive platform. Built on the robust **MERN Stack** (MongoDB, Express, React, Node.js), StudyOS features a modern **SaaS dashboard UI** inspired by **light neumorphism** to create a clean, fluid, and distraction-free environment for deep focus.

## ✨ Core Features

### 🖥️ Immersive Dashboard
The central hub of your academic life, designed for immediate insight and action.
- **Fluid Layout**: Dynamically expanding main content area that stretches intuitively when side panels are collapsed.
- **Floating Navigation**: A sleek, icon-only vertical dock that expands on hover to reveal full navigation labels without disrupting the main view.
- **Focus Timer (Pomodoro)**: A built-in, distraction-free timer to manage study blocks. Includes progress rings for active sessions.
- **Productivity Visualization**:
  - **Daily Goals**: Visual progress indicators tracking task completion.
  - **Activity Rings**: Elegant UI rings for Study Hours, Tasks Done, and Focus Score.
- **Smart Greetings**: Personalized welcome messages with a snapshot of pending tasks and current productivity status.

### 🛠️ Integrated Productivity Suite
Accessible instantly from the floating sidebar, these tools eliminate the need to switch apps:
- **📅 Academic Calendar**: Drag-and-drop scheduling for exams, assignments, and study blocks.
- **🧮 Scientific Calculator**: Embedded calculator for quick math, physics, and science computations without leaving the workspace.
- **📝 Sticky Notes**: A digital scratchpad for quick ideas, reminders, and temporary data.
- **🎨 Creative Drawing Pad**: A canvas for mind-mapping, sketching diagrams, or visual brainstorming.
- **✅ Smart Todo Lists**: Advanced task management with priority levels (High, Medium, Low), categories, and status tracking.

### 🎨 UI & Design Language
- **Modern SaaS Esthetics**: Clean, light theme relying on soft, neumorphism-inspired shadows (shadow-soft, shadow-inner) rather than harsh borders.
- **Premium Typography**: Driven by **Plus Jakarta Sans** for crisp, highly legible data presentation.
- **Micro-Interactions**: Smooth CSS transitions, dynamic flexbox DOM reflows (like w-80 to w-0 element collapsing), hover-expansion effects, and Framer Motion animations.
- **Responsive Layout**: Highly responsive design with absolute/fixed mobile positioning and a collapsible right info panel.

## 🏗️ Technical Architecture

### Frontend (Client)
- **Framework**: React 19 (via Vite) for blazing fast performance.
- **Styling Engine**: **Tailwind CSS v4**.
  - Uses modern CSS-first configurations (@theme variables in index.css).
  - Custom fluid flexbox layouts replacing traditional CSS grid rigid setups.
- **Motion Library**: Framer Motion for complex animations (entry transitions).
- **Icons**: Lucide React for consistent, lightweight visual cues.
- **State Management**: React Context API (AuthContext) for global user state.

### Backend (Server)
- **Runtime**: Node.js & Express.js.
- **Database**: MongoDB (NoSQL) for flexible data storage of users, tasks, and notes.
- **Authentication**: Secure JWT (JSON Web Token) implementation.
- **API Structure**: RESTful API endpoints organized by resource (/api/auth, /api/tasks, etc.).

## 🚀 Getting Started

### Prerequisites
- **Node.js**: v18.0.0 or higher.
- **MongoDB**: A running local instance or a cloud URI.
- **Git**: For version control.

### Installation

1. **Clone the Repository**
   `ash
   git clone https://github.com/yourusername/StudyOS.git
   cd StudyOS
   `

2. **Install Dependencies**
   
   **Client:**
   `ash
   cd client
   npm install
   `

   **Server:**
   `ash
   cd ../server
   npm install
   `

3. **Environment Configuration**
   Create a .env file in the server/ directory:
   `env
   PORT=5000
   MONGO_URI=mongodb://localhost:27017/studyos
   JWT_SECRET=your_super_secret_key_change_this
   `

4. **Launch the Application**
   You will need two terminal windows.

   **Terminal 1 (Backend):**
   `ash
   cd server
   npm start
   `

   **Terminal 2 (Frontend):**
   `ash
   cd client
   npm run dev
   `

## 📂 Folder Structure

`
StudyOS/
├── client/                     # React Frontend Application
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── assets/             # Images and global static files
│   │   ├── components/         # Reusable UI Blocks
│   │   │   ├── RightPanel.jsx  # Focus timer, Stats & user profile
│   │   │   ├── Sidebar.jsx     # Floating hover-expand navigation
│   │   │   └── ProtectedRoute.jsx # Auth Guard
│   │   ├── context/            # Global State
│   │   ├── pages/              # Main Route Views
│   │   │   ├── Dashboard.jsx   # Main Hub Layout
│   │   │   └── Login.jsx       # Auth Page
│   │   ├── index.css           # Tailwind v4 Theme & Neumorphism
│   │   └── main.jsx            # App Entry Point
│   ├── index.html              # HTML Root
│   └── vite.config.js          # Vite Bundler Config
│
└── server/                     # Express API Server
    ├── controllers/            # Request Handlers
    ├── middleware/             # Auth & Error middlewares
    ├── models/                 # Mongoose Data Schemas
    ├── routes/                 # API Routes
    └── index.js                # Server Entry & Config
`

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

*Built with ❤️ for the academic community.*
