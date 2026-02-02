import FileSaver from 'file-saver';

export const downloadFile = (content, filename, mimeType = 'text/plain;charset=utf-8') => {
  const blob = new Blob([content], { type: mimeType });
  FileSaver.saveAs(blob, filename);
};

export const downloadBlob = (blob, filename) => {
  FileSaver.saveAs(blob, filename);
};
