
import { BrowserRouter, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import type { AnalysisMode, SessionState } from './services/types';

// Components
import { Layout } from './components/Layout';

// Pages
import LandingPage from './pages/LandingPage';
import ModeSelection from './pages/ModeSelection';
import ResumeJobInput from './pages/ResumeJobInput';
import ParsedResumeReview from './pages/ParsedResumeReview';
import AnalysisProgress from './pages/AnalysisProgress';
import ResultsDashboard from './pages/ResultsDashboard';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Initial session state
const initialSessionState: SessionState = {
  sessionId: null,
  resume: null,
  jobDescription: null,
  evaluation: null,
  isLoading: false,
  error: null,
};

// Route to step mapping for V1
const routeToStep: Record<string, number> = {
  '/mode': 1,
  '/input': 2,
  '/review': 3,
  '/analyzing': 4,
  '/results': 5,
};



// Update Stepper definitions to match V1 flow
export const V1_STEPS = [
  { id: 1, name: 'Mode', description: 'Select mode' },
  { id: 2, name: 'Input', description: 'Resume & Job' },
  { id: 3, name: 'Review', description: 'Verify data' },
  { id: 4, name: 'Analyze', description: 'Processing' },
  { id: 5, name: 'Result', description: 'Fit score' },
];

function AppContent() {
  const [mode, setMode] = useState<AnalysisMode | null>(null);
  const [session, setSession] = useState<SessionState>(initialSessionState);
  const location = useLocation();
  const navigate = useNavigate();

  const currentStep = routeToStep[location.pathname] || 0;

  // Calculate completed steps based on session state
  const getCompletedSteps = (): number[] => {
    const completed: number[] = [];
    if (mode) completed.push(1);
    if (session.resume && session.jobDescription) completed.push(2);
    // Logic for step 3 completion (review) is largely implicit if we are at step 4
    if (currentStep > 3) completed.push(3);
    if (session.evaluation) completed.push(4, 5);
    return completed;
  };

  const resetSession = () => {
    setSession(initialSessionState);
    setMode(null);
    navigate('/');
  };



  // Determine if we should show back button
  const showBackButton = currentStep > 0 && location.pathname !== '/';
  const handleBack = () => navigate(-1);

  // Announce page changes for screen readers
  useEffect(() => {
    const pageName = V1_STEPS.find(s => s.id === currentStep)?.name || 'Page';
    document.title = `${pageName} - Smart Resume Analyzer`;
  }, [currentStep]);

  return (
    <Layout
      currentStep={currentStep}
      completedSteps={getCompletedSteps()}
      onReset={resetSession}
      showReset={!!session.sessionId}
      onBack={showBackButton ? handleBack : undefined}
      mode={mode}
    >
      <Routes>
        <Route path="/" element={<LandingPage />} />

        <Route
          path="/mode"
          element={
            <ModeSelection onModeSelect={(m) => {
              setMode(m);
              navigate('/input');
            }} />
          }
        />

        <Route
          path="/input"
          element={
            <ResumeJobInput
              session={session}
              setSession={setSession}
              mode={mode}
              onNext={() => {
                // Assisted mode skips review, goes directly to analyzing
                if (mode === 'assisted') {
                  navigate('/analyzing');
                } else {
                  navigate('/review');
                }
              }}
            />
          }
        />

        <Route
          path="/review"
          element={
            <ParsedResumeReview
              resume={session.resume}
              sessionId={session.sessionId || ''}
              onContinue={() => navigate('/analyzing')}
            />
          }
        />

        <Route
          path="/analyzing"
          element={
            <AnalysisProgress
              session={session}
              setSession={setSession}
            />
          }
        />

        <Route
          path="/results"
          element={
            <ResultsDashboard
              session={session}
              onStartOver={resetSession}
            />
          }
        />
      </Routes>
    </Layout>
  );
}

import { ErrorBoundary } from './components/ErrorBoundary';

// ... imports remain the same

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <BrowserRouter>
          <AppContent />
        </BrowserRouter>
      </ErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
