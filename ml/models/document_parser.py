"""
Policy Document Text Extraction
Extract text from PDF and DOCX files for downstream processing
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import json

# Optional dependencies - will show helpful error if not installed
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    pdfplumber = None

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    Document = None


class DocumentParser:
    """Extract text from PDF and DOCX files"""
    
    def __init__(self, output_dir="data/extracted_text"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_pdf(self, pdf_path: str) -> Dict:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dict containing extracted text and metadata
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError(
                "pdfplumber is not installed. Please install it with:\n"
                "pip install pdfplumber\n"
                "See FIX_IMPORTS.md for detailed installation instructions."
            )
        
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        extraction_result = {
            'file_name': pdf_path.name,
            'file_path': str(pdf_path),
            'format': 'pdf',
            'pages': [],
            'full_text': '',
            'total_pages': 0,
            'metadata': {}
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                extraction_result['total_pages'] = len(pdf.pages)
                extraction_result['metadata'] = pdf.metadata or {}
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        extraction_result['pages'].append({
                            'page_number': page_num,
                            'text': page_text.strip(),
                            'word_count': len(page_text.split())
                        })
                        extraction_result['full_text'] += page_text + '\n\n'
                
                extraction_result['full_text'] = extraction_result['full_text'].strip()
                
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
        
        return extraction_result
    
    def extract_docx(self, docx_path: str) -> Dict:
        """
        Extract text from DOCX file
        
        Args:
            docx_path: Path to DOCX file
            
        Returns:
            Dict containing extracted text and metadata
        """
        if not DOCX_AVAILABLE:
            raise ImportError(
                "python-docx is not installed. Please install it with:\n"
                "pip install python-docx\n"
                "See FIX_IMPORTS.md for detailed installation instructions."
            )
        
        docx_path = Path(docx_path)
        
        if not docx_path.exists():
            raise FileNotFoundError(f"DOCX file not found: {docx_path}")
        
        extraction_result = {
            'file_name': docx_path.name,
            'file_path': str(docx_path),
            'format': 'docx',
            'paragraphs': [],
            'full_text': '',
            'total_paragraphs': 0,
            'metadata': {}
        }
        
        try:
            doc = Document(docx_path)
            
            # Extract core properties
            extraction_result['metadata'] = {
                'author': doc.core_properties.author,
                'title': doc.core_properties.title,
                'subject': doc.core_properties.subject,
                'created': str(doc.core_properties.created),
                'modified': str(doc.core_properties.modified)
            }
            
            # Extract paragraphs
            for para_num, paragraph in enumerate(doc.paragraphs, 1):
                para_text = paragraph.text.strip()
                if para_text:  # Skip empty paragraphs
                    extraction_result['paragraphs'].append({
                        'paragraph_number': para_num,
                        'text': para_text,
                        'word_count': len(para_text.split())
                    })
                    extraction_result['full_text'] += para_text + '\n\n'
            
            extraction_result['full_text'] = extraction_result['full_text'].strip()
            extraction_result['total_paragraphs'] = len(extraction_result['paragraphs'])
            
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
        
        return extraction_result
    
    def extract_generic(self, file_path: str) -> Dict:
        """
        Auto-detect file type and extract text
        
        Args:
            file_path: Path to document file
            
        Returns:
            Dict containing extracted text and metadata
        """
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return self.extract_pdf(file_path)
        elif suffix in ['.docx', '.doc']:
            return self.extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Supported: .pdf, .docx")
    
    def save_extraction(self, extraction_result: Dict, output_name: str) -> Path:
        """
        Save extracted text to file
        
        Args:
            extraction_result: Result from extract_* methods
            output_name: Name for output file (without extension)
            
        Returns:
            Path to saved file
        """
        # Save as JSON
        json_path = self.output_dir / f"{output_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(extraction_result, f, indent=2, ensure_ascii=False)
        
        # Save plain text for easy reading
        txt_path = self.output_dir / f"{output_name}.txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(extraction_result['full_text'])
        
        print(f"✓ Saved extraction to:")
        print(f"  JSON: {json_path}")
        print(f"  TXT:  {txt_path}")
        
        return json_path


def main():
    """Example usage"""
    parser = DocumentParser()
    
    print("📄 CIVISIM Document Parser")
    print("=" * 50)
    
    # Example: Process a sample file if it exists
    sample_dir = Path("data/policy_samples")
    
    if sample_dir.exists():
        pdf_files = list(sample_dir.glob("*.pdf"))
        docx_files = list(sample_dir.glob("*.docx"))
        
        if pdf_files:
            print(f"\n✓ Found {len(pdf_files)} PDF file(s)")
            for pdf_file in pdf_files[:1]:  # Process first PDF
                print(f"\nProcessing: {pdf_file.name}")
                try:
                    result = parser.extract_pdf(pdf_file)
                    print(f"  Pages: {result['total_pages']}")
                    print(f"  Text length: {len(result['full_text'])} characters")
                    
                    # Save extraction
                    output_name = pdf_file.stem + "_extracted"
                    parser.save_extraction(result, output_name)
                except Exception as e:
                    print(f"  Error: {e}")
        
        if docx_files:
            print(f"\n✓ Found {len(docx_files)} DOCX file(s)")
            for docx_file in docx_files[:1]:  # Process first DOCX
                print(f"\nProcessing: {docx_file.name}")
                try:
                    result = parser.extract_docx(docx_file)
                    print(f"  Paragraphs: {result['total_paragraphs']}")
                    print(f"  Text length: {len(result['full_text'])} characters")
                    
                    # Save extraction
                    output_name = docx_file.stem + "_extracted"
                    parser.save_extraction(result, output_name)
                except Exception as e:
                    print(f"  Error: {e}")
    else:
        print("\n⚠️  No policy_samples directory found")
        print("   Create 'data/policy_samples' and add PDF/DOCX files")


if __name__ == "__main__":
    main()
