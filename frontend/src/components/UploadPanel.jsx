import React from 'react';

const acceptedFormats = '.png,.jpg,.jpeg,.pdf,.dwg,.dxf';

function UploadPanel({ label, onFileSelect, selectedFile }) {
  const handleChange = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const allowed = acceptedFormats.split(',');
    const ext = `.${file.name.split('.').pop().toLowerCase()}`;
    if (!allowed.includes(ext)) {
      alert('Please select a supported CAD/image file.');
      return;
    }
    onFileSelect(file);
  };

  return (
    <label className="group flex cursor-pointer flex-col items-center justify-center rounded-3xl border border-slate-800 bg-slate-900/80 p-6 text-center shadow-xl shadow-slate-950/30 transition hover:-translate-y-0.5 hover:border-cyan-400/60 hover:bg-slate-900">
      <div className="mb-3 rounded-full border border-cyan-500/20 bg-cyan-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">Upload</div>
      <div className="mb-2 text-xl font-semibold text-slate-100">{label}</div>
      <div className="mb-4 text-sm text-slate-400">Drop in a reference or comparison drawing</div>
      <input type="file" accept={acceptedFormats} onChange={handleChange} className="hidden" />
      <div className="w-full rounded-2xl border border-dashed border-slate-700 bg-slate-950/70 px-4 py-4 text-sm text-slate-300 transition group-hover:border-cyan-400/50">
        {selectedFile ? selectedFile.name : 'Choose a file'}
      </div>
      <div className="mt-3 text-xs text-slate-500">Supported: {acceptedFormats}</div>
    </label>
  );
}

export default UploadPanel;
