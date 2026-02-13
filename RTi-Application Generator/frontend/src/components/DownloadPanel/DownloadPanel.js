import React, { useState } from 'react';
import { downloadFile, downloadBlob } from '../../utils/fileDownload';
import { downloadDocument } from '../../services/draftService';
import { toast } from 'react-toastify';
import { FileText, Download } from 'lucide-react';
import './DownloadPanel.css';

const DownloadPanel = ({ draftData }) => {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (format) => {
    setDownloading(true);
    try {
      if (format === 'txt') {
        downloadFile(draftData.draft_text, 'draft_application.txt');
        toast.success("Downloaded as Text File");
      } else {
        // Pass all draftData to the service, which handles transformation
        const blob = await downloadDocument(draftData, format);
        
        const extension = format === 'excel' ? 'xlsx' : format;
        downloadBlob(blob, `application.${extension}`);
        toast.success(`Downloaded as ${format.toUpperCase()}`);
      }
    } catch (error) {
      toast.error(`Failed to download ${format.toUpperCase()}`);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="download-panel-card">
      <div className="panel-header">
        <h3><Download size={20} /> Download Options</h3>
        <p>Save your document in your preferred format</p>
      </div>
      
      <div className="download-grid">
        <button 
          className="download-btn pdf-btn" 
          onClick={() => handleDownload('pdf')}
          disabled={downloading}
        >
          <div className="download-btn__icon">PDF</div>
          <span>Portable Document</span>
        </button>

        <button 
          className="download-btn docx-btn" 
          onClick={() => handleDownload('docx')}
          disabled={downloading}
        >
          <div className="download-btn__icon">DOCX</div>
          <span>MS Word</span>
        </button>

        <button 
          className="download-btn txt-btn" 
          onClick={() => handleDownload('txt')}
          disabled={downloading}
        >
          <div className="download-btn__icon"><FileText size={24} /></div>
          <span>Plain Text</span>
        </button>
      </div>
    </div>
  );
};

export default DownloadPanel;
