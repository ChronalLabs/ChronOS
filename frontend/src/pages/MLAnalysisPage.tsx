import React, { useState } from 'react';
// Simple DJB2 hash for string
function hashPolicyText(text: string): string {
  let hash = 5381;
  for (let i = 0; i < text.length; i++) {
    hash = ((hash << 5) + hash) + text.charCodeAt(i);
  }
  return 'ml_analysis_' + (hash >>> 0); // unsigned
}
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { Sparkles, Brain, Workflow, FileText, AlertTriangle, CheckCircle2, Target, Shield, Zap, ArrowRight, Home, RefreshCw, BarChart3, Upload, File, X } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

interface MLAnalysisResult {
  success: boolean;
  policy_name: string;
  intent: {
    key_sentences: Array<{ sentence: string; importance: number }>;
    concepts: string[];
  };
  entities: Record<string, string[]>;
  ambiguity: {
    score: number;
    trust_level: string;
    by_severity: Record<string, number>;
    total_phrases: number;
    top_findings: Array<{ phrase: string; severity: string; context: string }>;
  };
  classification: {
    primary: string;
    confidence: number;
    recommendation: string;
  };
  parameters: {
    metadata: Record<string, any>;
    safety_profile: Record<string, any>;
    speed_profile: Record<string, any>;
    zone_constraints: Record<string, any>;
    simulation_params: Record<string, any>;
  };
  risk_assessment: {
    level: string;
    flags: Array<{ type: string; severity: string; message: string }>;
    is_acceptable: boolean;
    recommendation: string;
  };
  overall_summary: {
    policy_name: string;
    text_length: number;
    classification: string;
    confidence: number;
    ambiguity_score: number;
    trust_level: string;
    risk_level: string;
    entity_types_found: string[];
    total_entities: number;
    ready_for_simulation: boolean;
  };
}

// Premium glass card styling
const panelClass =
  'rounded-3xl border border-slate-200/60 bg-white/90 backdrop-blur-xl shadow-[0_32px_64px_rgba(15,23,42,0.12)] transition-all duration-300 hover:shadow-[0_40px_80px_rgba(15,23,42,0.15)]';

// Gradient text styling
const gradientText = 'bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent';

// Animated pulse for loading states
const pulseAnimation = 'animate-pulse';

const MLAnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  const [policyText, setPolicyText] = useState('');
  const [policyName, setPolicyName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<MLAnalysisResult | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<{ name: string; size: number } | null>(null);
  const [fileLoading, setFileLoading] = useState(false);
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  // File handling functions
  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const processFile = async (file: File) => {
    const allowedTypes = [
      'text/plain',
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    const allowedExtensions = ['.txt', '.pdf', '.doc', '.docx'];
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      setError(`Unsupported file type. Please upload TXT, PDF, DOC, or DOCX files.`);
      return;
    }

    setFileLoading(true);
    setError(null);

    try {
      if (file.type === 'text/plain' || fileExtension === '.txt') {
        // Handle TXT files directly
        const text = await file.text();
        setPolicyText(text);
        setUploadedFile({ name: file.name, size: file.size });
        if (!policyName) {
          setPolicyName(file.name.replace(/\.[^/.]+$/, ''));
        }
      } else if (fileExtension === '.pdf' || fileExtension === '.doc' || fileExtension === '.docx') {
        // Send PDF/DOC/DOCX files to backend for processing
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await axios.post(`${API_BASE}/ml/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        
        if (response.data.success && response.data.text) {
          setPolicyText(response.data.text);
          setUploadedFile({ name: file.name, size: file.size });
          if (!policyName) {
            setPolicyName(file.name.replace(/\.[^/.]+$/, ''));
          }
        } else {
          setError('Failed to extract text from file.');
        }
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to read file';
      setError(`Failed to read file: ${errorMessage}`);
    } finally {
      setFileLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  const clearUploadedFile = () => {
    setUploadedFile(null);
    setPolicyText('');
    setPolicyName('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  const pipelineHighlights = [
    {
      label: 'Intent Extraction',
      value: 'NLP Engine',
      helper: 'Key sentences & concept clustering',
      icon: <Brain size={20} />,
      gradient: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
      color: '#6366f1',
    },
    {
      label: 'Entity Recognition',
      value: 'NER Model',
      helper: 'Infrastructure, safety, fiscal signals',
      icon: <Target size={20} />,
      gradient: 'linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%)',
      color: '#0ea5e9',
    },
    {
      label: 'Risk Assessment',
      value: 'ML Classifier',
      helper: 'Severity flags with mitigation cues',
      icon: <Shield size={20} />,
      gradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
      color: '#f59e0b',
    },
    {
      label: 'Parameter Gen',
      value: 'Auto-Config',
      helper: 'Simulation-ready parameters',
      icon: <Zap size={20} />,
      gradient: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
      color: '#10b981',
    },
  ];

  const wordCount = policyText.trim() ? policyText.trim().split(/\s+/).length : 0;
  const isAnalyzeDisabled = loading || !policyText.trim();
  const entityEntries = result ? Object.entries(result.entities) : [];
  const severityEntries = result ? Object.entries(result.ambiguity.by_severity) : [];

  const samplePolicy = `Construction Policy: Urban Infrastructure Development Plan

SECTION 1: WORK HOURS AND SCHEDULING
Construction activities shall be permitted during extended hours from 6:00 AM to 10:00 PM on weekdays.
Night work may be authorized for critical infrastructure projects with proper noise mitigation measures.
Weekend work requires special permits and community notification at least 48 hours in advance.

SECTION 2: SAFETY REQUIREMENTS
All workers must complete OSHA-30 certification before working on elevated structures above 20 feet.
Hard hats, safety vests, and steel-toed boots are mandatory in all active construction zones.
Fall protection systems must be installed for any work performed at heights exceeding 6 feet.
Regular safety inspections shall be conducted weekly by certified safety officers.

SECTION 3: ENVIRONMENTAL PROTECTION
Dust control measures including water spraying must be implemented during dry conditions.
Noise levels shall not exceed 85 decibels at the project boundary during daytime hours.
Stormwater runoff must be managed through sediment basins and erosion control barriers.

SECTION 4: TRAFFIC MANAGEMENT
Lane closures on arterial roads require approval from the Traffic Management Center.
Flaggers must be present at all entry/exit points during peak traffic hours (7-9 AM, 4-6 PM).
Heavy equipment transport is restricted to off-peak hours to minimize traffic disruption.

SECTION 5: BUDGET AND TIMELINE
Total project budget: $45 million with 15% contingency reserve.
Estimated completion: 24 months from groundbreaking.
Milestone payments tied to completion of foundation, structural, and finishing phases.`;

  const handleAnalyze = async () => {
    if (!policyText.trim()) {
      setError('Please enter policy text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE}/ml/analyze`, {
        text: policyText,
        policy_name: policyName || 'Uploaded Policy'
      });
      setResult(response.data);

      // Persist ML analysis to localStorage keyed by policy text hash
      try {
        const mlStore = {
          policyName: response.data.policy_name,
          classification: response.data.classification.primary,
          confidence: response.data.classification.confidence,
          safetyProfile: response.data.parameters.safety_profile,
          speedProfile: response.data.parameters.speed_profile,
          zoneConstraints: response.data.parameters.zone_constraints,
          simulationParams: response.data.parameters.simulation_params,
          riskLevel: response.data.risk_assessment.level,
          trustLevel: response.data.overall_summary.trust_level,
          policyText: policyText,
        };
        const hashKey = hashPolicyText(policyText);
        localStorage.setItem(hashKey, JSON.stringify(mlStore));
        localStorage.setItem('ml_analysis_last_key', hashKey);
        // Also save a global copy for pages that read the canonical key
        localStorage.setItem('ml_analysis_params', JSON.stringify(mlStore));
      } catch (e) {
        console.warn('Failed to persist ML analysis to localStorage', e);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = () => {
    setPolicyText(samplePolicy);
    setPolicyName('Urban Infrastructure Development Plan');
  };

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'low':
        return 'text-emerald-700 bg-emerald-50 border border-emerald-200';
      case 'medium':
        return 'text-amber-700 bg-amber-50 border border-amber-200';
      case 'high':
        return 'text-orange-700 bg-orange-50 border border-orange-200';
      case 'critical':
        return 'text-red-700 bg-red-50 border border-red-200';
      default:
        return 'text-slate-700 bg-slate-100 border border-slate-200';
    }
  };

  const getTrustColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high':
        return 'text-emerald-600';
      case 'medium':
        return 'text-amber-600';
      case 'low':
        return 'text-rose-600';
      default:
        return 'text-slate-600';
    }
  };

  const scrollToInput = () => {
    document.getElementById('analysis-input')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="app" style={{ background: 'linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)' }}>
      {/* Premium Header with Gradient */}
      <header className="app-header" style={{ minHeight: '85vh', paddingBottom: '8rem' }}>
        <div className="app-header__bg" style={{ background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 30%, #ede9fe 70%, #e0e7ff 100%)' }} />
        <div className="app-header__glow app-header__glow--right" style={{ background: 'rgba(139, 92, 246, 0.25)', width: '24rem', height: '24rem' }} />
        <div className="app-header__glow app-header__glow--left" style={{ background: 'rgba(99, 102, 241, 0.2)', width: '28rem', height: '28rem' }} />
        
        {/* Decorative Elements */}
        <div style={{ position: 'absolute', top: '20%', right: '10%', width: '300px', height: '300px', background: 'radial-gradient(circle, rgba(139,92,246,0.08) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }} />
        <div style={{ position: 'absolute', bottom: '20%', left: '5%', width: '200px', height: '200px', background: 'radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%)', borderRadius: '50%', pointerEvents: 'none' }} />
        
        <div className="app-header__content">
          <nav className="navbar" style={{ paddingTop: '1.5rem' }}>
            <div className="navbar__brand">
              <div className="brand-icon" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', color: 'white', fontSize: '1.5rem' }}>🧠</div>
              <div className="brand-meta">
                <p className="brand-tagline" style={{ color: '#8b5cf6', fontWeight: '600' }}>MACHINE LEARNING LAB</p>
                <h1 className="brand-title" style={{ background: 'linear-gradient(135deg, #1e1b4b 0%, #4c1d95 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>CIVISIM</h1>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.75rem' }}>
              <button onClick={() => navigate('/')} className="secondary-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Home size={16} />
                Home
              </button>
              <button onClick={() => navigate('/simulation-engine')} className="nav-button" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                Simulation
                <ArrowRight size={16} />
              </button>
            </div>
          </nav>
  

          <div className="hero-grid" style={{ paddingTop: '3rem', display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
            <div className="hero-content hero-content--spread" style={{ textAlign: 'center', maxWidth: '900px', margin: '0 auto', padding: '0 1rem' }}>
              <p className="hero-badge" style={{ background: 'linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%)', color: '#7c3aed', border: '1px solid rgba(139,92,246,0.2)', margin: '0 auto', display: 'inline-flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem', borderRadius: '9999px', fontSize: '0.875rem', fontWeight: '600' }}>
                <Brain size={14} />
                AI-Powered Policy Analysis
              </p>
              <h2 className="hero-title hero-title--spread" style={{ fontSize: 'clamp(1.8rem, 5vw, 3.2rem)', lineHeight: '1.2', textAlign: 'center', marginTop: '1rem', fontWeight: '700' }}>
                Transform <span style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>policy documents</span> into simulation-ready intelligence
              </h2>
              <p className="hero-text hero-text--spread" style={{ fontSize: 'clamp(1rem, 2vw, 1.15rem)', color: '#475569', maxWidth: '750px', margin: '1.25rem auto 0', textAlign: 'center', lineHeight: '1.6' }}>
                Upload civic directives, extract operative intent, quantify ambiguity, and auto-generate
                simulation parameters. Built for policy strategists who demand clarity before commitments.
              </p>
              <div className="hero-actions hero-actions--spread" style={{ marginTop: '2rem', display: 'flex', flexWrap: 'wrap', gap: '1rem', justifyContent: 'center' }}>
                <button onClick={scrollToInput} className="primary-button" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)', padding: '1rem 2rem', fontSize: '1rem', boxShadow: '0 20px 40px rgba(139,92,246,0.3)', borderRadius: '12px', color: 'white', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <FileText size={18} />
                  Upload Policy
                </button>
                <button onClick={loadSample} className="secondary-button" style={{ padding: '1rem 2rem', borderRadius: '12px', background: 'white', border: '2px solid #e2e8f0', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Sparkles size={18} />
                  Load Sample
                </button>
              </div>
            </div>
            
            {/* Pipeline Preview Card - Horizontal Below */}
            <div
              className="summary-card"
              style={{ 
                background: 'rgba(255,255,255,0.95)', 
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(139,92,246,0.15)',
                boxShadow: '0 25px 60px rgba(139,92,246,0.12)',
                borderRadius: '24px',
                maxWidth: '1100px',
                margin: '0 auto',
                width: '100%',
                padding: '2rem'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(139,92,246,0.1)', paddingBottom: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                <span style={{ color: '#7c3aed', fontWeight: '700', fontSize: '1.1rem' }}>🔬 ML Analysis Pipeline</span>
                <span style={{ color: '#a78bfa', fontSize: '0.75rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>4-Stage Process</span>
              </div>
              <div
                style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}
              >
                {pipelineHighlights.map((tile, idx) => (
                  <div 
                    key={tile.label} 
                    style={{ 
                      background: 'linear-gradient(135deg, #ffffff 0%, #fafafa 100%)',
                      borderRadius: '16px',
                      padding: '1.5rem',
                      border: '2px solid rgba(0,0,0,0.05)',
                      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                      cursor: 'default',
                      position: 'relative'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateY(-4px)';
                      e.currentTarget.style.boxShadow = `0 12px 32px ${tile.color}30`;
                      e.currentTarget.style.borderColor = `${tile.color}40`;
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                      e.currentTarget.style.borderColor = 'rgba(0,0,0,0.05)';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', marginBottom: '1rem' }}>
                      <div style={{ 
                        width: '40px', 
                        height: '40px', 
                        borderRadius: '12px', 
                        background: tile.gradient,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white',
                        flexShrink: 0
                      }}>
                        {tile.icon}
                      </div>
                      <div style={{ flex: 1 }}>
                        <p style={{ margin: 0, fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: '700' }}>Stage {idx + 1}</p>
                        <p style={{ margin: '0.25rem 0 0', fontSize: '0.95rem', color: '#1e293b', fontWeight: '700' }}>{tile.label}</p>
                      </div>
                    </div>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#64748b', lineHeight: '1.5' }}>{tile.helper}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="app-main" style={{ marginTop: '-6rem', position: 'relative', zIndex: 10 }}>
        <div className="layout-container" style={{ paddingTop: '0', paddingBottom: '5rem', maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
          
          {/* Input Section with Premium Styling */}
          <section 
            id="analysis-input" 
            className={panelClass}
            style={{ 
              padding: '2.5rem',
              background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)',
              border: '1px solid rgba(139,92,246,0.1)'
            }}
          >
            {/* Section Header */}
            <div style={{ marginBottom: '2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                <div style={{ 
                  width: '42px', 
                  height: '42px', 
                  borderRadius: '12px', 
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <FileText size={22} />
                </div>
                <div>
                  <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '700', color: '#1e1b4b' }}>Policy Document</h2>
                  <p style={{ margin: 0, fontSize: '0.875rem', color: '#64748b' }}>Paste or upload your policy text for ML analysis</p>
                </div>
              </div>
            </div>

            {/* Policy Name Input */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                <input
                  type="text"
                  placeholder="📝 Policy Name (e.g., Urban Development Plan 2025)"
                  value={policyName}
                  onChange={(e) => setPolicyName(e.target.value)}
                  style={{
                    flex: '1',
                    minWidth: '280px',
                    padding: '1rem 1.25rem',
                    borderRadius: '14px',
                    border: '2px solid #e2e8f0',
                    background: 'white',
                    fontSize: '0.95rem',
                    color: '#1e293b',
                    transition: 'all 0.2s ease',
                    outline: 'none'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#8b5cf6';
                    e.target.style.boxShadow = '0 0 0 4px rgba(139,92,246,0.1)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = '#e2e8f0';
                    e.target.style.boxShadow = 'none';
                  }}
                />
                <button 
                  onClick={loadSample} 
                  className="secondary-button" 
                  style={{ 
                    padding: '1rem 1.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    background: 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)',
                    border: '2px solid #ddd6fe',
                    color: '#7c3aed',
                    fontWeight: '600'
                  }}
                >
                  <Sparkles size={16} />
                  Load Sample
                </button>
              </div>
            </div>

            {/* Drag & Drop Zone + Textarea */}
            <div style={{ marginBottom: '1.5rem' }}>
              {/* Hidden File Input */}
              <input
                ref={fileInputRef}
                type="file"
                accept=".txt,.pdf,.doc,.docx"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              
              {/* Drop Zone */}
              <div
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => !policyText && fileInputRef.current?.click()}
                style={{
                  padding: '2rem',
                  borderRadius: '16px',
                  border: `2px dashed ${isDragging ? '#8b5cf6' : '#cbd5e1'}`,
                  background: isDragging 
                    ? 'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)' 
                    : 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                  marginBottom: '1rem',
                  transition: 'all 0.3s ease',
                  cursor: policyText ? 'default' : 'pointer',
                  transform: isDragging ? 'scale(1.01)' : 'scale(1)',
                }}
              >
                {fileLoading ? (
                  <div style={{ textAlign: 'center', padding: '2rem' }}>
                    <div style={{ 
                      width: '48px', 
                      height: '48px', 
                      margin: '0 auto 1rem',
                      border: '3px solid #e2e8f0',
                      borderTopColor: '#8b5cf6',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite'
                    }} />
                    <p style={{ margin: 0, color: '#64748b', fontWeight: '500' }}>Processing file...</p>
                  </div>
                ) : uploadedFile ? (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'space-between',
                    padding: '0.5rem',
                    background: 'white',
                    borderRadius: '12px',
                    border: '1px solid #e2e8f0'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <div style={{ 
                        width: '40px', 
                        height: '40px', 
                        borderRadius: '10px', 
                        background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'white'
                      }}>
                        <File size={20} />
                      </div>
                      <div>
                        <p style={{ margin: 0, fontWeight: '600', color: '#1e293b', fontSize: '0.9rem' }}>{uploadedFile.name}</p>
                        <p style={{ margin: 0, fontSize: '0.75rem', color: '#64748b' }}>{formatFileSize(uploadedFile.size)}</p>
                      </div>
                    </div>
                    <button
                      onClick={(e) => { e.stopPropagation(); clearUploadedFile(); }}
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        border: 'none',
                        background: '#fee2e2',
                        color: '#ef4444',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseEnter={(e) => { e.currentTarget.style.background = '#fecaca'; }}
                      onMouseLeave={(e) => { e.currentTarget.style.background = '#fee2e2'; }}
                    >
                      <X size={16} />
                    </button>
                  </div>
                ) : (
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ 
                      width: '64px', 
                      height: '64px', 
                      margin: '0 auto 1rem',
                      borderRadius: '16px',
                      background: isDragging 
                        ? 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)' 
                        : 'linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: isDragging ? 'white' : '#64748b',
                      transition: 'all 0.3s ease'
                    }}>
                      <Upload size={28} />
                    </div>
                    <p style={{ 
                      margin: '0 0 0.5rem', 
                      fontWeight: '600', 
                      color: isDragging ? '#7c3aed' : '#334155',
                      fontSize: '1rem'
                    }}>
                      {isDragging ? 'Drop your file here!' : 'Drag & drop your policy document'}
                    </p>
                    <p style={{ margin: '0 0 1rem', fontSize: '0.85rem', color: '#64748b' }}>
                      or click to browse files
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                      {['TXT', 'PDF', 'DOC', 'DOCX'].map((format) => (
                        <span
                          key={format}
                          style={{
                            padding: '0.25rem 0.75rem',
                            borderRadius: '6px',
                            background: '#f1f5f9',
                            border: '1px solid #e2e8f0',
                            fontSize: '0.7rem',
                            fontWeight: '600',
                            color: '#64748b'
                          }}
                        >
                          .{format}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Or Divider */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '1rem',
                margin: '1.5rem 0'
              }}>
                <div style={{ flex: 1, height: '1px', background: '#e2e8f0' }} />
                <span style={{ fontSize: '0.8rem', color: '#94a3b8', fontWeight: '500' }}>OR PASTE TEXT BELOW</span>
                <div style={{ flex: 1, height: '1px', background: '#e2e8f0' }} />
              </div>
              
              {/* Textarea */}
              <div style={{ position: 'relative' }}>
                <textarea
                  placeholder="Paste your policy document text here...\n\nExample:\nSECTION 1: WORK HOURS\nConstruction activities shall be permitted during extended hours from 6:00 AM to 10:00 PM..."
                  value={policyText}
                  onChange={(e) => {
                    setPolicyText(e.target.value);
                    if (uploadedFile) setUploadedFile(null);
                  }}
                  style={{
                    width: '100%',
                    minHeight: '200px',
                    padding: '1.25rem',
                    borderRadius: '16px',
                    border: '2px solid #e2e8f0',
                    background: 'linear-gradient(180deg, #ffffff 0%, #fafafa 100%)',
                    fontSize: '0.9rem',
                    lineHeight: '1.7',
                    color: '#334155',
                    resize: 'vertical',
                    fontFamily: 'inherit',
                    transition: 'all 0.2s ease',
                    outline: 'none'
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = '#8b5cf6';
                    e.target.style.boxShadow = '0 0 0 4px rgba(139,92,246,0.08)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = '#e2e8f0';
                    e.target.style.boxShadow = 'none';
                  }}
                />
                {/* Word Count Badge */}
                <div style={{ 
                  position: 'absolute', 
                  bottom: '12px', 
                  right: '12px',
                  display: 'flex',
                  gap: '0.75rem',
                  background: 'rgba(255,255,255,0.95)',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0'
                }}>
                  <span style={{ fontSize: '0.75rem', color: '#94a3b8', fontWeight: '500' }}>
                    {policyText.length.toLocaleString()} chars
                  </span>
                  <span style={{ color: '#e2e8f0' }}>|</span>
                  <span style={{ fontSize: '0.75rem', color: '#8b5cf6', fontWeight: '600' }}>
                    {wordCount.toLocaleString()} words
                  </span>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                {policyText.length > 0 && (
                  <div style={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: '0.5rem',
                    padding: '0.5rem 1rem',
                    background: '#f0fdf4',
                    borderRadius: '8px',
                    border: '1px solid #bbf7d0'
                  }}>
                    <CheckCircle2 size={14} color="#22c55e" />
                    <span style={{ fontSize: '0.8rem', color: '#16a34a', fontWeight: '500' }}>Ready to analyze</span>
                  </div>
                )}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
                <button
                  onClick={() => {
                    setResult(null);
                    setPolicyText('');
                    setPolicyName('');
                  }}
                  className="secondary-button"
                  style={{ 
                    padding: '0.9rem 1.5rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}
                >
                  <RefreshCw size={16} />
                  Clear
                </button>
                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzeDisabled}
                  style={{ 
                    padding: '0.9rem 2rem',
                    background: isAnalyzeDisabled 
                      ? '#e2e8f0' 
                      : 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                    color: isAnalyzeDisabled ? '#94a3b8' : 'white',
                    border: 'none',
                    borderRadius: '12px',
                    fontSize: '0.95rem',
                    fontWeight: '600',
                    cursor: isAnalyzeDisabled ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    boxShadow: isAnalyzeDisabled ? 'none' : '0 8px 24px rgba(139,92,246,0.35)',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    if (!isAnalyzeDisabled) {
                      e.currentTarget.style.transform = 'translateY(-2px)';
                      e.currentTarget.style.boxShadow = '0 12px 32px rgba(139,92,246,0.4)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = isAnalyzeDisabled ? 'none' : '0 8px 24px rgba(139,92,246,0.35)';
                  }}
                >
                  {loading ? (
                    <>
                      <div style={{ 
                        width: '18px', 
                        height: '18px', 
                        border: '2px solid rgba(255,255,255,0.3)', 
                        borderTopColor: 'white',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite'
                      }} />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Brain size={18} />
                      Run ML Analysis
                      <ArrowRight size={16} />
                    </>
                  )}
                </button>
              </div>
            </div>
          </section>
          
          {/* Add keyframes for spinner */}
          <style>{`
            @keyframes spin {
              to { transform: rotate(360deg); }
            }
          `}</style>

          {/* Error Display */}
          {error && (
            <div 
              style={{ 
                marginTop: '2rem',
                padding: '1.25rem 1.5rem',
                background: 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                border: '2px solid #fca5a5',
                borderRadius: '16px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '1rem'
              }}
            >
              <div style={{ 
                width: '40px', 
                height: '40px', 
                borderRadius: '10px', 
                background: '#ef4444',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0
              }}>
                <AlertTriangle size={20} color="white" />
              </div>
              <div>
                <p style={{ margin: 0, fontWeight: '600', color: '#b91c1c', marginBottom: '0.25rem' }}>Analysis Failed</p>
                <p style={{ margin: 0, fontSize: '0.9rem', color: '#dc2626' }}>{error}</p>
              </div>
            </div>
          )}

          {/* Results Section */}
          {result && (
            <div style={{ marginTop: '2.5rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>
              
              {/* Success Banner */}
              <div 
                style={{ 
                  padding: '1rem 1.5rem',
                  background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
                  border: '2px solid #86efac',
                  borderRadius: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '1rem'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <CheckCircle2 size={24} color="#22c55e" />
                  <div>
                    <p style={{ margin: 0, fontWeight: '600', color: '#166534' }}>Analysis Complete!</p>
                    <p style={{ margin: 0, fontSize: '0.85rem', color: '#16a34a' }}>
                      Processed {result.overall_summary.text_length.toLocaleString()} characters in policy "{result.policy_name}"
                    </p>
                  </div>
                </div>
                <div
                  style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '8px',
                    fontWeight: '600',
                    fontSize: '0.85rem',
                    background: result.overall_summary.ready_for_simulation ? '#22c55e' : '#f59e0b',
                    color: 'white'
                  }}
                >
                  {result.overall_summary.ready_for_simulation ? '✓ Ready for Simulation' : '⚠ Needs Review'}
                </div>
              </div>

              {/* Summary Cards */}
              <section 
                className={panelClass}
                style={{ 
                  padding: '2rem',
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,250,255,0.95) 100%)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                  <div style={{ 
                    width: '38px', 
                    height: '38px', 
                    borderRadius: '10px', 
                    background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white'
                  }}>
                    <BarChart3 size={20} />
                  </div>
                  <h2 style={{ margin: 0, fontSize: '1.35rem', fontWeight: '700', color: '#1e1b4b' }}>Analysis Overview</h2>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
                  {/* Confidence Card */}
                  <div style={{ 
                    padding: '1.5rem',
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%)',
                    border: '1px solid #c7d2fe',
                    textAlign: 'center'
                  }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#4f46e5', marginBottom: '0.25rem' }}>
                      {(result.overall_summary.confidence * 100).toFixed(0)}%
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#6366f1', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Confidence</div>
                  </div>
                  
                  {/* Trust Level Card */}
                  <div style={{ 
                    padding: '1.5rem',
                    borderRadius: '16px',
                    background: result.overall_summary.trust_level.toLowerCase() === 'high' 
                      ? 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)'
                      : result.overall_summary.trust_level.toLowerCase() === 'medium'
                      ? 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)'
                      : 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                    border: result.overall_summary.trust_level.toLowerCase() === 'high' 
                      ? '1px solid #a7f3d0'
                      : result.overall_summary.trust_level.toLowerCase() === 'medium'
                      ? '1px solid #fcd34d'
                      : '1px solid #fca5a5',
                    textAlign: 'center'
                  }}>
                    <div style={{ 
                      fontSize: '2rem', 
                      fontWeight: '700', 
                      textTransform: 'capitalize',
                      color: result.overall_summary.trust_level.toLowerCase() === 'high' 
                        ? '#059669'
                        : result.overall_summary.trust_level.toLowerCase() === 'medium'
                        ? '#d97706'
                        : '#dc2626',
                      marginBottom: '0.25rem'
                    }}>
                      {result.overall_summary.trust_level}
                    </div>
                    <div style={{ fontSize: '0.8rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.8,
                      color: result.overall_summary.trust_level.toLowerCase() === 'high' 
                        ? '#059669'
                        : result.overall_summary.trust_level.toLowerCase() === 'medium'
                        ? '#d97706'
                        : '#dc2626'
                    }}>Trust Level</div>
                  </div>
                  
                  {/* Entities Card */}
                  <div style={{ 
                    padding: '1.5rem',
                    borderRadius: '16px',
                    background: 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
                    border: '1px solid #bae6fd',
                    textAlign: 'center'
                  }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: '700', color: '#0284c7', marginBottom: '0.25rem' }}>
                      {result.overall_summary.total_entities}
                    </div>
                    <div style={{ fontSize: '0.8rem', color: '#0369a1', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Entities Found</div>
                  </div>
                  
                  {/* Risk Level Card */}
                  <div style={{ 
                    padding: '1.5rem',
                    borderRadius: '16px',
                    background: result.overall_summary.risk_level.toLowerCase() === 'low'
                      ? 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)'
                      : result.overall_summary.risk_level.toLowerCase() === 'medium'
                      ? 'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)'
                      : 'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
                    border: result.overall_summary.risk_level.toLowerCase() === 'low'
                      ? '1px solid #a7f3d0'
                      : result.overall_summary.risk_level.toLowerCase() === 'medium'
                      ? '1px solid #fcd34d'
                      : '1px solid #fca5a5',
                    textAlign: 'center'
                  }}>
                    <div style={{ 
                      fontSize: '2rem', 
                      fontWeight: '700', 
                      textTransform: 'capitalize',
                      color: result.overall_summary.risk_level.toLowerCase() === 'low'
                        ? '#059669'
                        : result.overall_summary.risk_level.toLowerCase() === 'medium'
                        ? '#d97706'
                        : '#dc2626',
                      marginBottom: '0.25rem'
                    }}>
                      {result.overall_summary.risk_level}
                    </div>
                    <div style={{ fontSize: '0.8rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.8,
                      color: result.overall_summary.risk_level.toLowerCase() === 'low'
                        ? '#059669'
                        : result.overall_summary.risk_level.toLowerCase() === 'medium'
                        ? '#d97706'
                        : '#dc2626'
                    }}>Risk Level</div>
                  </div>
                </div>

                {/* Classification & Entity Types */}
                <div style={{ 
                  display: 'flex', 
                  flexWrap: 'wrap',
                  justifyContent: 'space-between', 
                  alignItems: 'center',
                  gap: '1.5rem',
                  padding: '1.5rem',
                  background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                  borderRadius: '16px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', minWidth: '200px' }}>
                    <span style={{ fontSize: '0.9rem', color: '#475569', fontWeight: '600' }}>Classification:</span>
                    <span style={{ 
                      padding: '0.5rem 1rem',
                      background: 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)',
                      color: 'white',
                      borderRadius: '8px',
                      fontSize: '0.9rem',
                      fontWeight: '700',
                      boxShadow: '0 4px 12px rgba(139,92,246,0.3)'
                    }}>{result.overall_summary.classification}</span>
                  </div>
                  <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: '0.5rem', flex: '1', minWidth: '300px' }}>
                    {result.overall_summary.entity_types_found.slice(0, 5).map((type) => (
                      <span
                        key={type}
                        style={{
                          padding: '0.4rem 0.8rem',
                          background: 'white',
                          border: '1px solid #cbd5e1',
                          borderRadius: '8px',
                          fontSize: '0.8rem',
                          color: '#334155',
                          fontWeight: '600'
                        }}
                      >
                        {type}
                      </span>
                    ))}
                    {result.overall_summary.entity_types_found.length > 5 && (
                      <span style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: '600' }}>
                        +{result.overall_summary.entity_types_found.length - 5} more
                      </span>
                    )}
                  </div>
                </div>
              </section>

              <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
                <div className={`${panelClass}`} style={{ padding: '2rem' }}>
                  <h3 style={{ marginBottom: '1.5rem', fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    🎯 Ambiguity Analysis
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
                    <div style={{ display: 'flex', width: '100%', justifyContent: 'center', gap: '2rem', flexWrap: 'wrap', alignItems: 'center' }}>
                      <div style={{ position: 'relative', width: '140px', height: '140px' }}>
                        <ResponsiveContainer>
                          <PieChart>
                            <Pie
                              data={[
                                { name: 'Ambiguous', value: result.ambiguity.score },
                                { name: 'Clear', value: 100 - result.ambiguity.score },
                              ]}
                              innerRadius={45}
                              outerRadius={60}
                              dataKey="value"
                            >
                              <Cell fill="#f97316" />
                              <Cell fill="#10b981" />
                            </Pie>
                          </PieChart>
                        </ResponsiveContainer>
                        <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                          <span style={{ fontSize: '2rem', fontWeight: '700', color: '#1e293b' }}>
                            {result.ambiguity.score.toFixed(0)}%
                          </span>
                          <span style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: '600', textTransform: 'uppercase' }}>Ambiguity</span>
                        </div>
                      </div>
                      <div style={{ flex: '1', minWidth: '200px', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                        {severityEntries.map(([severity, count]) => (
                          <div key={severity} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderRadius: '12px', border: '2px solid #f1f5f9', background: 'white', padding: '0.75rem 1rem', transition: 'all 0.2s ease' }}>
                            <span style={{ textTransform: 'capitalize', fontSize: '0.9rem', fontWeight: '600', color: '#475569' }}>{severity}</span>
                            <span style={{ fontSize: '1.1rem', fontWeight: '700', color: '#1e293b' }}>{count}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className={`${panelClass}`} style={{ padding: '2rem' }}>
                  <h3 style={{ marginBottom: '1.5rem', fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    🏷️ Entities Extracted
                  </h3>
                  <ResponsiveContainer width="100%" height={240}>
                    <BarChart data={entityEntries.map(([type, values]) => ({ name: type, count: values.length }))}>
                      <defs>
                        <linearGradient id="entityGradient" x1="0" x2="0" y1="0" y2="1">
                          <stop offset="0%" stopColor="#6366f1" stopOpacity={0.9} />
                          <stop offset="100%" stopColor="#38bdf8" stopOpacity={0.7} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="4 4" stroke="rgba(148,163,184,0.3)" />
                      <XAxis dataKey="name" stroke="rgba(71,85,105,0.8)" fontSize={12} />
                      <YAxis stroke="rgba(71,85,105,0.8)" />
                      <Tooltip
                        cursor={{ fill: 'rgba(99,102,241,0.08)' }}
                        contentStyle={{
                          backgroundColor: '#ffffff',
                          border: '1px solid rgba(148,163,184,0.35)',
                          borderRadius: '12px',
                          color: '#0f172a',
                          padding: '0.75rem'
                        }}
                      />
                      <Bar dataKey="count" fill="url(#entityGradient)" radius={[10, 10, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className={`${panelClass}`} style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
                  🎯 Key Policy Intentions
                </h3>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
                  {result.intent.concepts.map((concept, idx) => (
                    <span
                      key={idx}
                      style={{
                        borderRadius: '9999px',
                        border: '2px solid #c7d2fe',
                        background: 'linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%)',
                        padding: '0.5rem 1rem',
                        fontSize: '0.8rem',
                        fontWeight: '700',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                        color: '#4f46e5'
                      }}
                    >
                      {concept}
                    </span>
                  ))}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {result.intent.key_sentences.slice(0, 5).map((item, idx) => (
                    <div key={idx} style={{ borderRadius: '16px', border: '2px solid #e2e8f0', background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)', padding: '1.25rem' }}>
                      <div style={{ marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{ 
                          width: '100%', 
                          maxWidth: '200px',
                          height: '6px', 
                          background: '#f1f5f9', 
                          borderRadius: '999px',
                          overflow: 'hidden'
                        }}>
                          <div style={{ 
                            width: `${Math.round(item.importance * 100)}%`, 
                            height: '100%', 
                            background: 'linear-gradient(90deg, #8b5cf6 0%, #6366f1 100%)',
                            borderRadius: '999px'
                          }} />
                        </div>
                        <span style={{ fontSize: '0.75rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#6366f1' }}>
                          {Math.round(item.importance * 100)}% Important
                        </span>
                      </div>
                      <p style={{ margin: 0, fontSize: '0.95rem', lineHeight: '1.7', color: '#334155' }}>{item.sentence}</p>
                    </div>
                  ))}
                </div>
              </section>

              <section className={`${panelClass}`} style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
                  📋 Extracted Entities
                </h3>
                <div style={{ display: 'grid', gap: '1.25rem', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))' }}>
                  {entityEntries.map(([type, values]) => (
                    <div key={type} style={{ borderRadius: '16px', border: '2px solid #e2e8f0', background: 'white', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', transition: 'all 0.3s ease' }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-2px)';
                        e.currentTarget.style.boxShadow = '0 8px 24px rgba(99,102,241,0.12)';
                        e.currentTarget.style.borderColor = '#c7d2fe';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
                        e.currentTarget.style.borderColor = '#e2e8f0';
                      }}
                    >
                      <h4 style={{ marginBottom: '1rem', fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#6366f1' }}>
                        {type}
                      </h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.9rem', color: '#475569' }}>
                        {values.slice(0, 5).map((value, idx) => (
                          <div key={idx} style={{ display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
                            <span style={{ color: '#8b5cf6', fontWeight: '700' }}>•</span>
                            <span>{value}</span>
                          </div>
                        ))}
                        {values.length > 5 && (
                          <div style={{ fontSize: '0.75rem', color: '#94a3b8', fontStyle: 'italic', marginTop: '0.25rem' }}>+{values.length - 5} more entities</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <section className={`${panelClass}`} style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
                  ⚠️ Risk Assessment
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1.5rem', alignItems: 'start' }}>
                    <div className={`${getRiskColor(result.risk_assessment.level)}`} style={{ borderRadius: '16px', padding: '1.5rem 2rem', textAlign: 'center', minWidth: '200px', flex: '0 0 auto' }}>
                      <div style={{ fontSize: '2.5rem', fontWeight: '700', textTransform: 'capitalize', marginBottom: '0.25rem' }}>{result.risk_assessment.level}</div>
                      <div style={{ fontSize: '0.85rem', fontWeight: '600', opacity: 0.8 }}>Risk Level</div>
                    </div>
                    <div style={{ flex: '1', minWidth: '300px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                        {result.risk_assessment.flags.map((flag, idx) => (
                          <div key={idx} style={{ display: 'flex', alignItems: 'start', gap: '0.75rem' }}>
                            <span
                              style={{
                                borderRadius: '8px',
                                padding: '0.4rem 0.8rem',
                                fontSize: '0.75rem',
                                fontWeight: '700',
                                textTransform: 'uppercase',
                                letterSpacing: '0.05em',
                                flexShrink: 0,
                                ...(flag.severity === 'high'
                                  ? { border: '2px solid #fca5a5', background: '#fee2e2', color: '#dc2626' }
                                  : flag.severity === 'medium'
                                  ? { border: '2px solid #fcd34d', background: '#fef3c7', color: '#d97706' }
                                  : { border: '2px solid #93c5fd', background: '#dbeafe', color: '#1e40af' })
                              }}
                            >
                              {flag.severity}
                            </span>
                            <span style={{ fontSize: '0.9rem', lineHeight: '1.6', color: '#475569' }}>{flag.message}</span>
                          </div>
                        ))}
                      </div>
                      <div style={{ borderRadius: '16px', border: '2px solid #e2e8f0', background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)', padding: '1.25rem', fontSize: '0.9rem', color: '#475569', lineHeight: '1.6' }}>
                        <span style={{ fontWeight: '700', color: '#1e293b' }}>Recommendation:</span>{' '}
                        {result.risk_assessment.recommendation}
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              <section className={`${panelClass}`} style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                <h3 style={{ fontSize: '1.2rem', fontWeight: '700', color: '#1e293b', display: 'flex', alignItems: 'center', gap: '0.5rem', margin: 0 }}>
                  ⚙️ Generated Simulation Parameters
                </h3>
                <div style={{ display: 'grid', gap: '1.5rem', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h4 style={{ fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#64748b', margin: 0 }}>
                      Safety Profile
                    </h4>
                    <div style={{ borderRadius: '16px', border: '2px solid #e2e8f0', background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)', padding: '1.5rem' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.9rem', color: '#475569' }}>
                        {Object.entries(result.parameters.safety_profile).map(([key, value]) => (
                          <div key={key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f1f5f9' }}>
                            <span style={{ textTransform: 'capitalize', fontWeight: '500' }}>{key.replace(/_/g, ' ')}</span>
                            <span style={{ fontFamily: 'monospace', fontWeight: '700', color: '#1e293b', fontSize: '0.95rem' }}>{String(value)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h4 style={{ fontSize: '0.85rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#64748b', margin: 0 }}>
                      Speed Profile
                    </h4>
                    <div style={{ borderRadius: '16px', border: '2px solid #e2e8f0', background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)', padding: '1.5rem' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.9rem', color: '#475569' }}>
                        {Object.entries(result.parameters.speed_profile).map(([key, value]) => (
                          <div key={key} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f1f5f9' }}>
                            <span style={{ textTransform: 'capitalize', fontWeight: '500' }}>{key.replace(/_/g, ' ')}</span>
                            <span style={{ fontFamily: 'monospace', fontWeight: '700', color: '#1e293b', fontSize: '0.95rem' }}>{String(value)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </section>

              {/* Final Action Buttons - Next Steps */}
              <section 
                className={panelClass}
                style={{ 
                  padding: '2rem',
                  background: 'linear-gradient(135deg, rgba(236,253,245,0.9) 0%, rgba(209,250,229,0.9) 100%)',
                  border: '2px solid #86efac'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                  <div style={{ 
                    width: '42px', 
                    height: '42px', 
                    borderRadius: '12px', 
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white'
                  }}>
                    <ArrowRight size={22} />
                  </div>
                  <div>
                    <h2 style={{ margin: 0, fontSize: '1.35rem', fontWeight: '700', color: '#065f46' }}>What's Next?</h2>
                    <p style={{ margin: 0, fontSize: '0.875rem', color: '#047857' }}>Your policy analysis is complete. Choose your next step:</p>
                  </div>
                </div>
                
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
                  {/* Run Simulation Option */}
                  <button 
                    onClick={() => {
                      // Save ML parameters to localStorage for simulation, keyed by policy text hash
                      const mlParams = {
                        policyName: result.policy_name,
                        classification: result.classification.primary,
                        confidence: result.classification.confidence,
                        safetyProfile: result.parameters.safety_profile,
                        speedProfile: result.parameters.speed_profile,
                        zoneConstraints: result.parameters.zone_constraints,
                        simulationParams: result.parameters.simulation_params,
                        riskLevel: result.risk_assessment.level,
                        trustLevel: result.overall_summary.trust_level,
                        policyText: policyText // store for hash lookup
                      };
                      const hashKey = hashPolicyText(policyText);
                      localStorage.setItem(hashKey, JSON.stringify(mlParams));
                      localStorage.setItem('ml_analysis_last_key', hashKey); // for quick lookup
                      navigate('/simulation-engine');
                    }}
                    style={{ 
                      padding: '1.5rem',
                      background: 'white',
                      border: '2px solid #10b981',
                      borderRadius: '16px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s ease',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.75rem'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                      e.currentTarget.style.color = 'white';
                      e.currentTarget.style.transform = 'translateY(-3px)';
                      e.currentTarget.style.boxShadow = '0 12px 32px rgba(16,185,129,0.35)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'white';
                      e.currentTarget.style.color = 'inherit';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <Workflow size={24} />
                      <span style={{ fontSize: '1.1rem', fontWeight: '700' }}>Run Simulation</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.8 }}>
                      Use the extracted parameters to simulate policy impacts on traffic, safety, and costs.
                    </p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: '600', textTransform: 'uppercase' }}>Recommended</span>
                      <ArrowRight size={14} />
                    </div>
                  </button>
                  
                  {/* Configure Policy Option */}
                  <button 
                    onClick={() => {
                      // Save ML parameters for policy configuration, keyed by policy text hash
                      const mlParams = {
                        policyName: result.policy_name,
                        classification: result.classification.primary,
                        parameters: result.parameters,
                        policyText: policyText
                      };
                      const hashKey = hashPolicyText(policyText);
                      localStorage.setItem(hashKey, JSON.stringify(mlParams));
                      localStorage.setItem('ml_analysis_last_key', hashKey);
                      navigate('/policy-config');
                    }}
                    style={{ 
                      padding: '1.5rem',
                      background: 'white',
                      border: '2px solid #8b5cf6',
                      borderRadius: '16px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s ease',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.75rem'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)';
                      e.currentTarget.style.color = 'white';
                      e.currentTarget.style.transform = 'translateY(-3px)';
                      e.currentTarget.style.boxShadow = '0 12px 32px rgba(139,92,246,0.35)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'white';
                      e.currentTarget.style.color = 'inherit';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <Target size={24} />
                      <span style={{ fontSize: '1.1rem', fontWeight: '700' }}>Configure Policy</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.8 }}>
                      Fine-tune the extracted parameters before running simulations.
                    </p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: '600', textTransform: 'uppercase' }}>Customize</span>
                      <ArrowRight size={14} />
                    </div>
                  </button>
                  
                  {/* View Impact Analysis Option */}
                  <button 
                    onClick={() => navigate('/impact-analysis')}
                    style={{ 
                      padding: '1.5rem',
                      background: 'white',
                      border: '2px solid #0ea5e9',
                      borderRadius: '16px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      transition: 'all 0.3s ease',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.75rem'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)';
                      e.currentTarget.style.color = 'white';
                      e.currentTarget.style.transform = 'translateY(-3px)';
                      e.currentTarget.style.boxShadow = '0 12px 32px rgba(14,165,233,0.35)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'white';
                      e.currentTarget.style.color = 'inherit';
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.boxShadow = 'none';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <BarChart3 size={24} />
                      <span style={{ fontSize: '1.1rem', fontWeight: '700' }}>View Impact Analysis</span>
                    </div>
                    <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.8 }}>
                      Compare previous simulation results and analyze policy impacts.
                    </p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: '600', textTransform: 'uppercase' }}>Compare</span>
                      <ArrowRight size={14} />
                    </div>
                  </button>
                </div>
                
                {/* Secondary Actions */}
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'center', 
                  gap: '1rem',
                  marginTop: '1.5rem',
                  paddingTop: '1.5rem',
                  borderTop: '1px solid #a7f3d0'
                }}>
                  <button
                    onClick={() => {
                      setResult(null);
                      setPolicyText('');
                      setPolicyName('');
                      scrollToInput();
                    }}
                    style={{ 
                      padding: '0.75rem 1.5rem',
                      background: 'transparent',
                      color: '#047857',
                      border: '1px solid #86efac',
                      borderRadius: '10px',
                      fontSize: '0.9rem',
                      fontWeight: '600',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#ecfdf5';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'transparent';
                    }}
                  >
                    <RefreshCw size={16} />
                    Analyze Another Policy
                  </button>
                  <button
                    onClick={() => navigate('/')}
                    style={{ 
                      padding: '0.75rem 1.5rem',
                      background: 'transparent',
                      color: '#047857',
                      border: '1px solid #86efac',
                      borderRadius: '10px',
                      fontSize: '0.9rem',
                      fontWeight: '600',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      transition: 'all 0.2s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#ecfdf5';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'transparent';
                    }}
                  >
                    <Home size={16} />
                    Back to Home
                  </button>
                </div>
              </section>
            </div>
          )}
        </div>
      </main>
      
      {/* Footer */}
      <footer style={{ 
        padding: '2.5rem 1rem',
        textAlign: 'center',
        borderTop: '1px solid #e2e8f0',
        background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)'
      }}>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#64748b', fontWeight: '500' }}>
          🧠 CIVISIM ML Lab • AI-Powered Policy Analysis Engine
        </p>
      </footer>
    </div>
  );
};

export default MLAnalysisPage;
