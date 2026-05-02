export interface DatasetPreviewResponse {
  columns: string[];
  rows: any[];
  totalRows: number;
}

export interface AnalysisResponse {
  stats: any;
  charts: any;
  insights: string[];
}
