import React from 'react';
import type { ReportMetric } from '../types';

export const AnomalyCard: React.FC<{ metric: ReportMetric }> = ({ metric }) => {
  const isPositive = metric.delta_pct > 0;
  return (
    <div className="p-4 border rounded-lg bg-white shadow-sm flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-500">{metric.metric_name}</p>
        <p className="text-2xl font-bold">{metric.current_value.toLocaleString()}</p>
      </div>
      <div className={`px-3 py-1 rounded-full text-sm font-medium ${isPositive ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
        {isPositive ? '↑' : '↓'} {Math.abs(metric.delta_pct)}%
      </div>
    </div>
  );
};
