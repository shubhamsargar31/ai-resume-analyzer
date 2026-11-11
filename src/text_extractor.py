"""
Text Extraction Module for AI Resume Analyzer.
Extracts raw text from PDF and DOCX files safely in-memory without persistent disk storage.
"""

import io
import os
from typing import Union, Tuple, Optional

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None


class ResumeExtractionError(Exception):
    """Custom exception raised when resume text extraction fails."""
    pass


def extract_text_from_pdf(file_input: Union[str, bytes, io.BytesIO]) -> str:
    """
    Extracts text from a PDF file using pypdf.
    
    Args:
        file_input: File path, bytes, or BytesIO stream of the PDF.
        
    Returns:
        Extracted text as a clean string.
        
    Raises:
        ResumeExtractionError: If file is corrupted, encrypted, or cannot be read.
    """
    if PdfReader is None:
        raise ResumeExtractionError("pypdf is not installed. Please install it with 'pip install pypdf'.")
    
    try:
        if isinstance(file_input, (bytes, bytearray)):
            stream = io.BytesIO(file_input)
        elif isinstance(file_input, io.BytesIO):
            stream = file_input
            stream.seek(0)
        elif isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise ResumeExtractionError(f"File not found: {file_input}")
            stream = open(file_input, "rb")
        else:
            # E.g. Streamlit UploadedFile
            stream = io.BytesIO(file_input.read())
            file_input.seek(0)

        reader = PdfReader(stream)
        
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception:
                raise ResumeExtractionError("The uploaded PDF is password-protected and cannot be read.")

        text_pages = []
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_pages.append(page_text.strip())

        if isinstance(file_input, str) and hasattr(stream, 'close'):
            stream.close()

        full_text = "\n\n".join(text_pages)
        if not full_text.strip():
            raise ResumeExtractionError("PDF file appears to be empty or contains scanned images without selectable text.")

        return full_text

    except ResumeExtractionError:
        raise
    except Exception as e:
        raise ResumeExtractionError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_input: Union[str, bytes, io.BytesIO]) -> str:
    """
    Extracts text from a DOCX file using python-docx.
    
    Args:
        file_input: File path, bytes, or BytesIO stream of the DOCX.
        
    Returns:
        Extracted text as a clean string.
        
    Raises:
        ResumeExtractionError: If file is invalid or cannot be read.
    """
    if docx is None:
        raise ResumeExtractionError("python-docx is not installed. Please install it with 'pip install python-docx'.")
    
    try:
        if isinstance(file_input, (bytes, bytearray)):
            stream = io.BytesIO(file_input)
        elif isinstance(file_input, io.BytesIO):
            stream = file_input
            stream.seek(0)
        elif isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise ResumeExtractionError(f"File not found: {file_input}")
            stream = file_input
        else:
            # Streamlit UploadedFile
            stream = io.BytesIO(file_input.read())
            file_input.seek(0)

        doc = docx.Document(stream)
        text_blocks = []

        # Extract text from paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_blocks.append(paragraph.text.strip())

        # Extract text from tables (many resumes format skills or experience in tables)
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    text_blocks.append(" | ".join(row_cells))

        full_text = "\n".join(text_blocks)
        if not full_text.strip():
            raise ResumeExtractionError("DOCX file appears to be empty.")

        return full_text

    except ResumeExtractionError:
        raise
    except Exception as e:
        raise ResumeExtractionError(f"Failed to extract text from DOCX: {str(e)}")


def extract_resume_text(uploaded_file, file_name: Optional[str] = None) -> Tuple[str, str]:
    """
    Unified extraction entry point. Automatically identifies format and extracts text.
    
    Args:
        uploaded_file: Uploaded file object, bytes, or file path.
        file_name: Optional explicit file name (if uploaded_file is raw bytes or stream).
        
    Returns:
        Tuple of (extracted_text, file_type).
        
    Raises:
        ResumeExtractionError: If format is unsupported or extraction fails.
    """
    name = file_name or getattr(uploaded_file, "name", "") or (uploaded_file if isinstance(uploaded_file, str) else "")
    name_lower = name.lower()

    if name_lower.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
        return text, "PDF"
    elif name_lower.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
        return text, "DOCX"
    elif name_lower.endswith(".txt"):
        if hasattr(uploaded_file, "read"):
            content = uploaded_file.read()
            uploaded_file.seek(0)
            if isinstance(content, bytes):
                text = content.decode("utf-8", errors="ignore")
            else:
                text = str(content)
        elif isinstance(uploaded_file, str):
            with open(uploaded_file, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        else:
            text = str(uploaded_file)
        if not text.strip():
            raise ResumeExtractionError("Text file is empty.")
        return text, "TXT"
    else:
        raise ResumeExtractionError(
            f"Unsupported file format '{name}'. Please upload a standard PDF (.pdf) or Microsoft Word (.docx) resume."
        )
