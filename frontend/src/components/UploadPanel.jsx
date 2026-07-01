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
    <label className="relative group flex cursor-pointer flex-col items-center justify-center overflow-hidden rounded-3xl border border-slate-700/50 bg-slate-800/20 p-8 text-center shadow-2xl backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-cyan-500/50 hover:bg-slate-800/40 hover:shadow-[0_0_30px_-5px_rgba(34,211,238,0.2)]">
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
      <div className="relative flex flex-col items-center w-full">
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 transition-transform duration-300 group-hover:scale-110 group-hover:bg-cyan-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <div className="mb-2 font-display text-2xl font-semibold tracking-wide text-slate-100">{label}</div>
        <div className="mb-6 text-sm text-slate-400">Drag and drop or click to browse</div>
        <input type="file" accept={acceptedFormats} onChange={handleChange} className="hidden" />
        <div className="w-full rounded-2xl border border-dashed border-slate-600/50 bg-slate-900/50 px-6 py-4 text-sm font-medium text-slate-300 transition-colors duration-300 group-hover:border-cyan-500/50 group-hover:text-cyan-100">
          {selectedFile ? (
            <span className="flex items-center justify-center gap-2 text-cyan-300 truncate px-2">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 shrink-0" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              <span className="truncate">{selectedFile.name}</span>
            </span>
          ) : (
            'Select a file...'
          )}
        </div>
        <div className="mt-4 text-xs font-medium uppercase tracking-wider text-slate-500">Supported: {acceptedFormats}</div>
      </div>
    </label>
  );
}

export default UploadPanel;
