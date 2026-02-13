import React from 'react'
import { ShieldAlert, CheckCircle } from 'lucide-react'
import { SimulationAnalysis } from '../types/simulation'

interface Props {
  analysis?: SimulationAnalysis
}

const ExplanationCard: React.FC<Props> = ({ analysis }) => {
  if (!analysis) {
    return (
      <div className="empty-panel">
        Narrative insight will appear after a scenario completes.
      </div>
    )
  }

  const isUnsafe = analysis.verdict?.toUpperCase() === 'UNSAFE'

  return (
    <div className={`explanation-card ${isUnsafe ? 'is-unsafe' : ''}`}>
      <div className="explanation-header">
        {isUnsafe ? (
          <ShieldAlert size={40} color="#dc2626" />
        ) : (
          <CheckCircle size={40} color="#059669" />
        )}
        <div>
          <p className="verdict-tag">Verdict</p>
          <h3 className="verdict-title">{analysis.verdict}</h3>
          <p className="verdict-summary">{analysis.summary}</p>
          <p className="verdict-quote">"{analysis.trade_offs}"</p>

          {analysis.warnings?.length > 0 && (
            <div className="warning-block">
              <p className="warning-block__title">Ethical warnings</p>
              <ul className="warning-list">
                {analysis.warnings.map((warning) => (
                  <li key={warning}>• {warning}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ExplanationCard