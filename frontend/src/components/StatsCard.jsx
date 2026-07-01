import React from 'react';

function StatsCard({ statistics }) {
  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900/80 p-6 shadow-lg">
      <h3 className="mb-4 text-lg font-semibold">Difference Statistics</h3>
      <div className="mb-4 grid gap-4 md:grid-cols-2">
        <div className="rounded-xl bg-slate-800 p-4">
          <div className="text-sm text-slate-400">Changed regions</div>
          <div className="text-2xl font-semibold">{statistics?.num_changed_regions ?? 0}</div>
        </div>
        <div className="rounded-xl bg-slate-800 p-4">
          <div className="text-sm text-slate-400">Area changed</div>
          <div className="text-2xl font-semibold">{statistics?.percent_area_changed ?? 0}%</div>
        </div>
      </div>
      <div className="overflow-hidden rounded-xl border border-slate-800">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-800 text-left text-slate-300">
            <tr>
              <th className="px-3 py-2">Location</th>
              <th className="px-3 py-2">Type</th>
              <th className="px-3 py-2">Area px</th>
            </tr>
          </thead>
          <tbody>
            {(statistics?.regions || []).map((region, index) => (
              <tr key={`${region.location}-${index}`} className="border-t border-slate-800 bg-slate-900/50">
                <td className="px-3 py-2">{region.location}</td>
                <td className="px-3 py-2">{region.type}</td>
                <td className="px-3 py-2">{region.area_px}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StatsCard;
