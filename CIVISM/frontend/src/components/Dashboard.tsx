import React, { useEffect, useState } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line,
} from 'recharts'
import { SimulationResults } from '../types/simulation'

interface DashboardProps {
  data: SimulationResults | null
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  if (!data) {
    return (
      <div className="empty-panel">
        Run a simulation to unlock comparative insights.
      </div>
    )
  }

  const { baseline, policy } = data

  const [chartsReady, setChartsReady] = useState(false)
  useEffect(() => {
    const frame = requestAnimationFrame(() => setChartsReady(true))
    return () => cancelAnimationFrame(frame)
  }, [])

  const comparisonData = [
    {
      name: 'Duration (Days)',
      Baseline: baseline.metrics.duration,
      Proposed: policy.metrics.duration,
    },
    {
      name: 'Risk Score (0-100)',
      Baseline: baseline.metrics.risk_score,
      Proposed: policy.metrics.risk_score,
    },
    {
      name: 'Disruption (0-100)',
      Baseline: baseline.metrics.disruption_index,
      Proposed: policy.metrics.disruption_index,
    },
  ]

  const metricCards = [
    {
      label: 'Duration',
      value: `${policy.metrics.duration} d`,
      baseline: baseline.metrics.duration,
      pulse: policy.metrics.duration <= baseline.metrics.duration,
      descriptor: policy.metrics.duration <= baseline.metrics.duration ? 'Faster than baseline' : 'Slower than baseline',
    },
    {
      label: 'Accident Risk',
      value: `${policy.metrics.risk_score} / 100`,
      baseline: baseline.metrics.risk_score,
      pulse: policy.metrics.risk_score <= 50,
      descriptor: policy.metrics.risk_score <= 50 ? 'Within safe corridor' : 'Monitor closely',
    },
    {
      label: 'Civic Disruption',
      value: `${policy.metrics.disruption_index} / 100`,
      baseline: baseline.metrics.disruption_index,
      pulse: policy.metrics.disruption_index <= baseline.metrics.disruption_index,
      descriptor: policy.metrics.disruption_index <= baseline.metrics.disruption_index ? 'Public tolerance improving' : 'Elevated disruption',
    },
  ]

  return (
    <div className="dashboard">
      <div className="metric-grid">
        {metricCards.map((card) => (
          <div key={card.label} className="metric-card">
            <p className="metric-card__title">{card.label}</p>
            <p className="metric-card__value">{card.value}</p>
            <p className="metric-card__baseline">Baseline: {card.baseline}</p>
            <p
              className={`metric-card__status ${
                card.pulse ? 'metric-card__status--positive' : 'metric-card__status--negative'
              }`}
            >
              {card.descriptor}
            </p>
          </div>
        ))}
      </div>

      <div className="chart-grid">
        <div className="chart-panel">
          <h3 className="chart-panel__title">Impact Comparison</h3>
          <div className="chart-surface">
            {chartsReady ? (
              <ResponsiveContainer width="100%" height="100%" minWidth={260} minHeight={220}>
                <BarChart data={comparisonData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.3)" />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: '#475569', fontSize: 12 }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <YAxis
                    stroke="#94a3b8"
                    tick={{ fill: '#475569', fontSize: 12 }}
                    tickLine={false}
                    axisLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      background: '#ffffff',
                      border: '1px solid rgba(148,163,184,0.35)',
                      borderRadius: '16px',
                      color: '#0f172a',
                    }}
                  />
                  <Legend wrapperStyle={{ color: '#475569' }} />
                  <Bar dataKey="Baseline" fill="#475569" radius={[8, 8, 8, 8]} />
                  <Bar dataKey="Proposed" fill="#6366F1" radius={[8, 8, 8, 8]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="chart-placeholder" />
            )}
          </div>
        </div>

        <div className="chart-panel">
          <h3 className="chart-panel__title">Project Timeline Projection</h3>
          <div className="chart-surface">
            {chartsReady ? (
              <ResponsiveContainer width="100%" height="100%" minWidth={260} minHeight={220}>
                <LineChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.3)" />
                  <XAxis
                    dataKey="day"
                    type="number"
                    allowDuplicatedCategory={false}
                    stroke="#94a3b8"
                    tick={{ fill: '#475569', fontSize: 12 }}
                  />
                  <YAxis
                    dataKey="progress"
                    unit="%"
                    stroke="#94a3b8"
                    tick={{ fill: '#475569', fontSize: 12 }}
                  />
                  <Tooltip
                    contentStyle={{
                      background: '#ffffff',
                      border: '1px solid rgba(148,163,184,0.35)',
                      borderRadius: '16px',
                      color: '#0f172a',
                    }}
                  />
                  <Legend wrapperStyle={{ color: '#475569' }} />
                  <Line
                    data={baseline.timeline}
                    type="monotone"
                    dataKey="progress"
                    name="Baseline"
                    stroke="#94a3b8"
                    dot={false}
                    strokeWidth={2}
                  />
                  <Line
                    data={policy.timeline}
                    type="monotone"
                    dataKey="progress"
                    name="Proposed"
                    stroke="#6366f1"
                    dot={false}
                    strokeWidth={3}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="chart-placeholder" />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard