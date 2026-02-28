import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Sidebar from "./components/Sidebar";
import RightPanel from "./components/RightPanel";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Subjects from "./pages/Subjects";
import CalendarPage from "./pages/Calendar";
import Calculator from "./pages/Calculator";
import StickyNotes from "./pages/StickyNotes";
import Notepad from "./pages/Notepad";
import TodoList from "./pages/TodoList";
import DrawingPad from "./pages/DrawingPad";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/subjects" element={<Subjects />} />
            <Route path="/calendar" element={<CalendarPage />} />
            <Route path="/calculator" element={<Calculator />} />
            <Route path="/sticky-notes" element={<StickyNotes />} />
            <Route path="/notes" element={<Notepad />} />
            <Route path="/todos" element={<TodoList />} />
            <Route path="/drawing-pad" element={<DrawingPad />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          </Route>

          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
