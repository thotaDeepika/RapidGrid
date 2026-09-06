import React from 'react';
import { BrainCircuit, Star } from 'lucide-react';

export default function AIRationale({ plan }) {
  if (!plan) return null;

  return (
    <div className="bg-white p-6 rounded-3xl border border-[#e2e8f0] shadow-elevation-md flex flex-col gap-4 relative overflow-hidden">
      {/* Decorative background accent */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-[#f0ecfd] rounded-full blur-2xl pointer-events-none" />
      
      <div className="flex justify-between items-center z-10 border-b border-[#e2e8f0] pb-3">
        <h3 className="font-display font-extrabold flex items-center gap-2 text-[#5f4bb6] text-base">
          <BrainCircuit size={20} />
          Decision Fusion AI Rationale
        </h3>
        <div className="flex items-center gap-1.5 bg-[#f0ecfd] text-[#5f4bb6] px-3 py-1 rounded-full text-xs font-bold font-mono border border-[#86a5d9]/30">
          <Star size={14} className="fill-[#5f4bb6]" />
          {Math.round((plan.overall_confidence || 0.94) * 100)}% Confidence
        </div>
      </div>
      
      <p className="text-xs text-[#5a6860] z-10 leading-relaxed bg-[#f6f8fb] p-3.5 rounded-2xl border border-[#e2e8f0] font-body">
        {plan.explanation}
      </p>

      <div className="z-10 space-y-2">
        <h4 className="text-[11px] font-mono font-bold text-[#5f4bb6] uppercase tracking-wider">5-Dimension Factor Scoring Breakdown</h4>
        <div className="bg-[#f6f8fb] rounded-2xl border border-[#e2e8f0] overflow-hidden">
          <table className="w-full text-xs text-left">
            <thead className="bg-[#f0f4f9] text-[10px] font-mono uppercase text-[#5a6860] border-b border-[#e2e8f0]">
              <tr>
                <th className="px-3.5 py-2 font-bold">Factor</th>
                <th className="px-3.5 py-2 font-bold text-center">Weight</th>
                <th className="px-3.5 py-2 font-bold text-right">Weighted Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e2e8f0] font-mono">
              {plan.factor_breakdown?.map((f, i) => (
                <tr key={i} className="text-[#202a25] hover:bg-[#f0ecfd]/50 transition-colors">
                  <td className="px-3.5 py-2 font-semibold">{f.factor}</td>
                  <td className="px-3.5 py-2 text-center text-[#5a6860]">{f.weight.toFixed(2)}</td>
                  <td className="px-3.5 py-2 text-right font-bold text-[#5f4bb6]">{f.weighted_score.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
