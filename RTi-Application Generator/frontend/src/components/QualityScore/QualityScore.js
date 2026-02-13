import React from 'react';
import { CheckCircle, AlertCircle, AlertTriangle, Info, Shield, FileText, Building, Target } from 'lucide-react';
import './QualityScore.css';

const CATEGORY_ICONS = {
  legal: Shield,
  clarity: Target,
  completeness: FileText,
  authority: Building,
  format: FileText
};

const CATEGORY_LABELS = {
  legal: { en: 'Legal Compliance', hi: 'कानूनी अनुपालन' },
  clarity: { en: 'Clarity', hi: 'स्पष्टता' },
  completeness: { en: 'Completeness', hi: 'पूर्णता' },
  authority: { en: 'Authority', hi: 'प्राधिकरण' },
  format: { en: 'Format', hi: 'प्रारूप' }
};

const QualityScore = ({ 
  score, 
  grade, 
  issues = [], 
  scoresBreakdown = {}, 
  summary,
  summaryHi,
  language = 'english',
  onIssueClick 
}) => {
  const isHindi = language === 'hindi';

  const getGradeColor = (grade) => {
    switch (grade) {
      case 'A': return 'grade-a';
      case 'B': return 'grade-b';
      case 'C': return 'grade-c';
      case 'D': return 'grade-d';
      case 'F': return 'grade-f';
      default: return '';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'error': return <AlertCircle size={14} />;
      case 'warning': return <AlertTriangle size={14} />;
      case 'info': return <Info size={14} />;
      default: return <Info size={14} />;
    }
  };

  const errorCount = issues.filter(i => i.severity === 'error').length;
  const warningCount = issues.filter(i => i.severity === 'warning').length;
  const infoCount = issues.filter(i => i.severity === 'info').length;

  return (
    <div className="quality-score-panel">
      {/* Main Score Display */}
      <div className="score-header">
        <div className={`score-circle ${getGradeColor(grade)}`}>
          <span className="score-value">{score}</span>
          <span className="score-grade">{grade}</span>
        </div>
        <div className="score-summary">
          <h3>{isHindi ? 'गुणवत्ता स्कोर' : 'Quality Score'}</h3>
          <p className="summary-text">{isHindi ? summaryHi : summary}</p>
          <div className="issue-counts">
            {errorCount > 0 && (
              <span className="count error">
                <AlertCircle size={12} /> {errorCount} {isHindi ? 'त्रुटि' : 'error'}{errorCount > 1 && !isHindi ? 's' : ''}
              </span>
            )}
            {warningCount > 0 && (
              <span className="count warning">
                <AlertTriangle size={12} /> {warningCount} {isHindi ? 'चेतावनी' : 'warning'}{warningCount > 1 && !isHindi ? 's' : ''}
              </span>
            )}
            {infoCount > 0 && (
              <span className="count info">
                <Info size={12} /> {infoCount} {isHindi ? 'सुझाव' : 'suggestion'}{infoCount > 1 && !isHindi ? 's' : ''}
              </span>
            )}
            {errorCount === 0 && warningCount === 0 && (
              <span className="count success">
                <CheckCircle size={12} /> {isHindi ? 'कोई समस्या नहीं' : 'No issues'}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="score-breakdown">
        <h4>{isHindi ? 'श्रेणी विश्लेषण' : 'Category Breakdown'}</h4>
        <div className="breakdown-bars">
          {Object.entries(scoresBreakdown).map(([category, categoryScore]) => {
            const Icon = CATEGORY_ICONS[category] || FileText;
            const label = CATEGORY_LABELS[category] || { en: category, hi: category };
            
            return (
              <div key={category} className="breakdown-item">
                <div className="breakdown-label">
                  <Icon size={14} />
                  <span>{isHindi ? label.hi : label.en}</span>
                </div>
                <div className="breakdown-bar-container">
                  <div 
                    className={`breakdown-bar ${categoryScore >= 80 ? 'good' : categoryScore >= 50 ? 'fair' : 'poor'}`}
                    style={{ width: `${categoryScore}%` }}
                  />
                </div>
                <span className="breakdown-value">{categoryScore}%</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Issues List */}
      {issues.length > 0 && (
        <div className="issues-section">
          <h4>{isHindi ? 'समस्याएं और सुझाव' : 'Issues & Suggestions'}</h4>
          <div className="issues-list">
            {issues.map((issue, idx) => (
              <div 
                key={idx} 
                className={`issue-item ${issue.severity}`}
                onClick={() => onIssueClick && onIssueClick(issue)}
              >
                <div className="issue-icon">
                  {getSeverityIcon(issue.severity)}
                </div>
                <div className="issue-content">
                  <span className="issue-message">{issue.message}</span>
                  {issue.suggestion && (
                    <span className="issue-suggestion">
                      💡 {issue.suggestion}
                    </span>
                  )}
                  {issue.field && (
                    <span className="issue-field">
                      {isHindi ? 'फ़ील्ड:' : 'Field:'} {issue.field}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pass/Fail Indicator */}
      <div className={`validity-indicator ${errorCount === 0 ? 'pass' : 'fail'}`}>
        {errorCount === 0 ? (
          <>
            <CheckCircle size={18} />
            <span>{isHindi ? 'ड्राफ्ट जनरेट करने के लिए तैयार' : 'Ready to Generate Draft'}</span>
          </>
        ) : (
          <>
            <AlertCircle size={18} />
            <span>{isHindi ? 'आगे बढ़ने से पहले त्रुटियां ठीक करें' : 'Fix Errors Before Proceeding'}</span>
          </>
        )}
      </div>
    </div>
  );
};

export default QualityScore;
