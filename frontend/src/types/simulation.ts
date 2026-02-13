export type SafetyLevel = 'low' | 'standard' | 'high'
export type UrgencyLevel = 'standard' | 'high'
export type LaborAvailability = 'standard' | 'increased'
export type TrafficManagement = 'basic' | 'advanced'

export interface SimulationConfig {
  night_shifts: boolean
  safety_level: SafetyLevel
  urgency: UrgencyLevel
  labor: LaborAvailability
  traffic: TrafficManagement
}

export interface SimulationMetrics {
  duration: number
  risk_score: number
  disruption_index: number
}

export interface TimelinePoint {
  day: number
  progress: number
}

export interface SimulationScenario {
  metrics: SimulationMetrics
  timeline: TimelinePoint[]
}

export interface SimulationAnalysis {
  verdict: string
  summary: string
  trade_offs: string
  warnings: string[]
}

export interface SimulationResults {
  baseline: SimulationScenario
  policy: SimulationScenario
  analysis: SimulationAnalysis
  timestamp?: string
}
