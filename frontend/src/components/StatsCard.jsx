import React from 'react';

function StatsCard({ statistics }) {
  return (
    <div className="rounded-3xl border border-slate-700/50 bg-slate-800/20 p-8 shadow-2xl backdrop-blur-xl">
      <div className="mb-6 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/20 text-cyan-400">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
          </svg>
        </div>
        <h3 className="font-display text-2xl font-semibold text-slate-100">Difference Statistics</h3>
      </div>

      <div className="mb-8 grid gap-4 sm:grid-cols-2">
        <div className="group relative overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-900/50 p-6 transition-all hover:border-cyan-500/50">
          <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-cyan-500/10 blur-2xl transition-all group-hover:bg-cyan-500/20" />
          <div className="relative">
            <div className="text-sm font-medium tracking-wide text-slate-400 uppercase">Changed regions</div>
            <div className="mt-2 font-display text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">{statistics?.num_changed_regions ?? 0}</div>
          </div>
        </div>
        <div className="group relative overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-900/50 p-6 transition-all hover:border-purple-500/50">
          <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-purple-500/10 blur-2xl transition-all group-hover:bg-purple-500/20" />
          <div className="relative">
            <div className="text-sm font-medium tracking-wide text-slate-400 uppercase">Area changed</div>
            <div className="mt-2 font-display text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">{statistics?.percent_area_changed ?? 0}%</div>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-700/50 bg-slate-900/40">
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-800/80 text-left text-xs font-semibold uppercase tracking-wider text-slate-400 backdrop-blur-md">
              <tr>
                <th className="px-6 py-4">Location</th>
                <th className="px-6 py-4">Type</th>
                <th className="px-6 py-4">Dimensions (WxH)</th>
                <th className="px-6 py-4">Area px</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {(statistics?.regions || []).map((region, index) => (
                <tr key={`${region.location}-${index}`} className="transition-colors hover:bg-slate-800/40">
                  <td className="whitespace-nowrap px-6 py-4 font-medium text-slate-300">{region.location}</td>
                  <td className="whitespace-nowrap px-6 py-4">
                    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold tracking-wide border ${
                      region.type === 'added' ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400' :
                      region.type === 'removed' ? 'border-red-500/30 bg-red-500/10 text-red-400' :
                      'border-amber-500/30 bg-amber-500/10 text-amber-400'
                    }`}>
                      {region.type.toUpperCase()}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-6 py-4 text-slate-400 font-mono">{region.width && region.height ? `${region.width} × ${region.height}` : 'N/A'}</td>
                  <td className="whitespace-nowrap px-6 py-4 text-slate-400 font-mono">{region.area_px}</td>
                </tr>
              ))}
              {(!statistics?.regions || statistics.regions.length === 0) && (
                <tr>
                  <td colSpan="4" className="px-6 py-8 text-center text-slate-500 italic">No regions found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default StatsCard;
