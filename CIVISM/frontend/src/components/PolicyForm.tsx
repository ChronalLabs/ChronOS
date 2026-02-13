import React from 'react'
import { Settings } from 'lucide-react'
import {
  SimulationConfig,
  SafetyLevel,
  UrgencyLevel,
  LaborAvailability,
  TrafficManagement,
} from '../types/simulation'

interface PolicyProps {
  config: SimulationConfig
  setConfig: (c: SimulationConfig) => void
  onSimulate: () => void
  isLoading: boolean
}

const safetyOptions: { label: string; value: SafetyLevel; note: string }[] = [
  { label: 'Low · Cost cutting', value: 'low', note: 'Minimal compliance, fastest pace' },
  { label: 'Standard · BIS baseline', value: 'standard', note: 'Balanced controls + cost' },
  { label: 'High · International', value: 'high', note: 'Maximum guardrails, higher spend' },
]

const urgencyOptions: { label: string; value: UrgencyLevel; note: string }[] = [
  { label: 'Standard timeline', value: 'standard', note: 'Civic-friendly delivery' },
  { label: 'Election deadline', value: 'high', note: 'Accelerated crews & shifts' },
]

const laborOptions: { label: string; value: LaborAvailability; note: string }[] = [
  { label: 'Standard crews', value: 'standard', note: 'Baseline staffing levels' },
  { label: 'Increased labor', value: 'increased', note: 'Overlapping shifts, contract surge' },
]

const trafficOptions: { label: string; value: TrafficManagement; note: string }[] = [
  { label: 'Basic management', value: 'basic', note: 'Barricades + signage only' },
  { label: 'Advanced plan', value: 'advanced', note: 'Dynamic rerouting + wardens' },
]

const PolicyForm: React.FC<PolicyProps> = ({ config, setConfig, onSimulate, isLoading }) => {
  const toggleNightShifts = (value: boolean) => setConfig({ ...config, night_shifts: value })

  return (
    <section className="policy-card">
      <div className="policy-header">
        <div className="policy-header__icon">
          <Settings size={20} />
        </div>
        <div className="policy-header__meta">
          <h2 className="policy-title">Policy Controls</h2>
          <p className="policy-subtitle">Input stack</p>
        </div>
      </div>

      <p className="policy-description">
        Tune the levers that matter to civic safety boards. CIVISIM will re-run your active blueprint instantly.
      </p>

      {/* Two-column grid layout for all policy sections */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem', marginBottom: '1.5rem' }}>
        
        {/* Night construction */}
        <div className="policy-section">
          <p className="policy-section__title">Night construction</p>
          <p className="policy-section__note">Extend permissible hours to compress the schedule.</p>
          <div className="option-grid option-grid--split">
            {[
              {
                label: '24x7 enabled',
                value: true,
                sub: 'Requires community consent',
              },
              {
                label: 'Daylight only',
                value: false,
                sub: 'Standard civic ordinance',
              },
            ].map((option) => {
              const isActive = config.night_shifts === option.value
              return (
                <button
                  key={option.label}
                  type="button"
                  onClick={() => toggleNightShifts(option.value)}
                  className={`option-button option-accent-blue ${isActive ? 'is-active' : ''}`}
                >
                  <p className="option-button__title">{option.label}</p>
                  <p className="option-button__note">{option.sub}</p>
                </button>
              )
            })}
          </div>
        </div>

        {/* Safety doctrine */}
        <div className="policy-section">
          <p className="policy-section__title">Safety doctrine</p>
          <p className="policy-section__note">Select the compliance rigor enforced on site.</p>
          <div className="option-grid">
            {safetyOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setConfig({ ...config, safety_level: option.value })}
                className={`option-button option-accent-emerald ${
                  config.safety_level === option.value ? 'is-active' : ''
                }`}
              >
                <p className="option-button__title">{option.label}</p>
                <p className="option-button__note">{option.note}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Political urgency */}
        <div className="policy-section">
          <p className="policy-section__title">Political urgency</p>
          <p className="policy-section__note">Align delivery commitments with stakeholder pressure.</p>
          <div className="option-grid">
            {urgencyOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setConfig({ ...config, urgency: option.value })}
                className={`option-button option-accent-amber ${
                  config.urgency === option.value ? 'is-active' : ''
                }`}
              >
                <p className="option-button__title">{option.label}</p>
                <p className="option-button__note">{option.note}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Labor availability */}
        <div className="policy-section">
          <p className="policy-section__title">Labor availability</p>
          <p className="policy-section__note">Scale up crews to compress timelines, noting fatigue trade-offs.</p>
          <div className="option-grid">
            {laborOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setConfig({ ...config, labor: option.value })}
                className={`option-button option-accent-sky ${
                  config.labor === option.value ? 'is-active' : ''
                }`}
              >
                <p className="option-button__title">{option.label}</p>
                <p className="option-button__note">{option.note}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Traffic management - span full width */}
        <div className="policy-section" style={{ gridColumn: '1 / -1' }}>
          <p className="policy-section__title">Traffic management intensity</p>
          <p className="policy-section__note">Mitigate disruption through smarter diversions and wardens.</p>
          <div className="option-grid option-grid--split">
            {trafficOptions.map((option) => (
              <button
                key={option.value}
                type="button"
                onClick={() => setConfig({ ...config, traffic: option.value })}
                className={`option-button option-accent-purple ${
                  config.traffic === option.value ? 'is-active' : ''
                }`}
              >
                <p className="option-button__title">{option.label}</p>
                <p className="option-button__note">{option.note}</p>
              </button>
            ))}
          </div>
        </div>
      </div>

      <button onClick={onSimulate} disabled={isLoading} className="policy-submit">
        {isLoading ? 'Simulating scenario...' : 'Run Simulation'}
      </button>
    </section>
  )
}

export default PolicyForm