import React from 'react';
import { BrainCircuit, Star } from 'lucide-react';

export default function AIRationale({ plan }) {
  if (!plan) return null;

  return (
    <div className="glass-card bg-[#1e293b] border-amber-500/30 flex flex-col gap-4 relative overflow-hidden">
      {/* Decorative background glow */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-amber-500/10 rounded-full blur-3xl" />
      
      <div className="flex justify-between items-center z-10">
        <h3 className="font-bold flex items-center gap-2 text-amber-400">
          <BrainCircuit size={20} />
          AI Rationale
        </h3>
        <div className="flex items-center gap-1 bg-amber-500/20 text-amber-400 px-3 py-1 rounded-full text-sm font-bold border border-amber-500/30">
          <Star size={14} className="fill-amber-400" />
          {Math.round(plan.overall_confidence * 100)}% Confidence
        </div>
      </div>
      
      <p className="text-sm text-gray-300 z-10 leading-relaxed">
        {plan.explanation}
      </p>

      <div className="mt-2 z-10">
        <h4 className="text-xs font-bold text-gray-400 mb-2 uppercase tracking-wider">Hospital Factor Breakdown</h4>
        <div className="bg-slate-900/50 rounded-lg border border-slate-700/50 overflow-hidden">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-800/80 text-xs text-gray-400">
              <tr>
                <th className="px-3 py-2 font-medium">Factor</th>
                <th className="px-3 py-2 font-medium text-center">Weight</th>
                <th className="px-3 py-2 font-medium text-right">Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700/50">
              {plan.factor_breakdown?.map((f, i) => (
                <tr key={i} className="text-gray-300">
                  <td className="px-3 py-2">{f.factor}</td>
                  <td className="px-3 py-2 text-center text-gray-500">{f.weight.toFixed(2)}</td>
                  <td className="px-3 py-2 text-right font-bold text-amber-400/90">{f.weighted_score.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
