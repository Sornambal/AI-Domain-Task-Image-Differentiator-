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
    <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-slate-700 bg-slate-900/80 p-6 text-center shadow-lg transition hover:border-cyan-400">
      <div className="mb-3 text-lg font-semibold">{label}</div>
      <div className="mb-3 text-sm text-slate-400">Upload a reference or comparison drawing</div>
      <input type="file" accept={acceptedFormats} onChange={handleChange} className="hidden" />
      <div className="rounded-lg border border-dashed border-slate-600 px-4 py-3 text-sm text-slate-300">
        {selectedFile ? selectedFile.name : 'Choose file'}
      </div>
      <div className="mt-2 text-xs text-slate-500">Supported: {acceptedFormats}</div>
    </label>
  );
}

export default UploadPanel;
