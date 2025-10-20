# autograder_simplified.py
# Simplified autograder - NO LangGraph, NO file system operations, NO database
# Accepts submissions via request body only
# Supports: PDF, Word (.docx), Python (.py), and text files

import os
import re
import io
import base64
from typing import Optional, Dict, Any
import fitz  # PyMuPDF for PDF extraction
from openai import OpenAI

# Try to import docx for Word document support
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
MODEL_NAME = "gpt-4o"
client = OpenAI(api_key=OPENAI_API_KEY)
print("OPENAI_API_KEY: ", OPENAI_API_KEY)
# No Tesseract needed - we only support text-based files


# ============================================================================
# HELPER FUNCTIONS (No Database)
# ============================================================================

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        return f"⚠️ PDF extraction failed: {e}"


def extract_text_from_docx_bytes(docx_bytes: bytes) -> str:
    """Extract text from Word document bytes."""
    if not DOCX_AVAILABLE:
        return "⚠️ Word document support not available. Install python-docx: pip install python-docx"
    
    try:
        doc = Document(io.BytesIO(docx_bytes))
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"⚠️ Word document extraction failed: {e}"


def detect_content_type(text: str) -> str:
    """
    Detect if text is code, math, or normal text.
    Simplified heuristic-based detection.
    """
    if not text or not text.strip():
        return "text"
    
    # Check for code keywords
    code_keywords = [
        "def ", "class ", "import ", "print(", "if ", "for ", "while ",
        "function", "const ", "let ", "var ", "public ", "private ",
        "return ", "void ", "#include"
    ]
    if any(k in text for k in code_keywords):
        return "code"
    
    # Check for math symbols/patterns
    math_indicators = ["=", "∫", "∑", "√", "π", "sin", "cos", "tan", "log", "lim", "dx", "dy"]
    if any(m in text for m in math_indicators):
        # More specific check: count math vs regular equals
        if text.count("=") > 2 or any(m in text for m in ["∫", "∑", "√", "π", "lim"]):
            return "math"
    
    return "text"


def generate_ai_feedback(content_type: str, text: str) -> Dict[str, Any]:
    """
    Generate AI feedback using OpenAI.
    Returns: {"feedback": str, "grade": int or None, "tokens": int, "cost": float}
    
    NOTE: No database calls - all token tracking removed from this function
    """
    # Check if API key is configured
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-":
        return {
            "feedback": "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable. See FIX_API_KEY.md for instructions.",
            "grade": None,
            "tokens": 0,
            "cost": 0.0
        }
    
    try:
        system_prompt = f"""You are an expert {content_type} grader. 
Give informative, constructive feedback in 30-50 words.
Always respond in plain text ending with the line:
'FINAL GRADE: <number>/100'

Example:
---
## FEEDBACK
The code meets most requirements but lacks edge case handling and comments.
Consider adding input validation.
FINAL GRADE: 87/100
---
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.1,
            max_tokens=1500
        )
        
        feedback_text = response.choices[0].message.content
        
        # Calculate token usage and cost
        usage = getattr(response, "usage", None)
        tokens_used = 0
        cost = 0.0
        
        if usage:
            tokens_used = usage.total_tokens
            # Approximate cost for gpt-4o: $0.005 per 1K input, $0.015 per 1K output
            cost = (usage.prompt_tokens * 0.005 + usage.completion_tokens * 0.015) / 1000
        
        # Extract grade from feedback
        grade = None
        match = re.search(r"(\d{1,3})\s*/\s*100", feedback_text)
        if match:
            grade = int(match.group(1))
        
        return {
            "feedback": feedback_text,
            "grade": grade,
            "tokens": tokens_used,
            "cost": round(cost, 6)
        }
    
    except Exception as e:
        return {
            "feedback": f"⚠️ AI feedback failed: {e}",
            "grade": None,
            "tokens": 0,
            "cost": 0.0
        }


# ============================================================================
# SIMPLIFIED AUTOGRADER PIPELINE (No LangGraph)
# ============================================================================

def autograde_text(content: str, content_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Simplified autograder - single function, no graph complexity.
    
    Args:
        content: The text content to grade (code, math, essay, etc.)
        content_type: Optional type hint ("code", "math", "text"). Auto-detected if None.
    
    Returns:
        {
            "detected_type": str,
            "feedback": str,
            "grade": int or None,
            "tokens": int,
            "cost": float
        }
    """
    # Step 1: Detect content type if not provided
    detected_type = content_type if content_type else detect_content_type(content)
    
    # Step 2: Generate AI feedback
    result = generate_ai_feedback(detected_type, content)
    
    # Step 3: Return result
    return {
        "detected_type": detected_type,
        "feedback": result["feedback"],
        "grade": result["grade"],
        "tokens": result["tokens"],
        "cost": result["cost"]
    }


def autograde_pdf(pdf_bytes: bytes) -> Dict[str, Any]:
    """Grade a PDF submission (extracts text first)."""
    text = extract_text_from_pdf_bytes(pdf_bytes)
    return autograde_text(text)


def autograde_docx(docx_bytes: bytes) -> Dict[str, Any]:
    """Grade a Word document submission."""
    text = extract_text_from_docx_bytes(docx_bytes)
    return autograde_text(text)


def autograde_file(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Grade any file based on extension.
    
    Supports:
    - PDF files (.pdf)
    - Word documents (.docx, .doc)
    - Python files (.py)
    - Text files (.txt, .java, .cpp, .js, etc.)
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith(".pdf"):
        return autograde_pdf(file_bytes)
    
    elif filename_lower.endswith((".docx", ".doc")):
        return autograde_docx(file_bytes)
    
    else:
        # Text-based files (.py, .txt, .java, .cpp, .js, etc.)
        try:
            text = file_bytes.decode("utf-8")
        except:
            text = file_bytes.decode("latin-1", errors="ignore")
        return autograde_text(text)


def autograde_base64(base64_string: str, file_type: str = "text") -> Dict[str, Any]:
    """
    Grade a base64-encoded file.
    
    Args:
        base64_string: Base64-encoded file content
        file_type: "pdf", "docx", or "text"
    """
    try:
        file_bytes = base64.b64decode(base64_string)
    except Exception as e:
        return {
            "detected_type": "error",
            "feedback": f"Invalid base64 data: {e}",
            "grade": None,
            "tokens": 0,
            "cost": 0.0
        }
    
    if file_type == "pdf":
        return autograde_pdf(file_bytes)
    elif file_type == "docx":
        return autograde_docx(file_bytes)
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
        return autograde_text(text)


# ============================================================================
# EXAMPLE USAGE (Standalone)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" SIMPLIFIED AUTOGRADER - Supports PDF, Word (.docx), Python (.py)")
    print(" No OCR/Image support - Text-based files only")
    print("=" * 70)
    
    # Example 1: Grade Python code
    code_sample = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

result = bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(result)
"""
    
    print("\n" + "=" * 60)
    print("Example 1: Grading Python code")
    print("=" * 60)
    result = autograde_text(code_sample, content_type="code")
    print(f"Type: {result['detected_type']}")
    print(f"Grade: {result['grade']}/100")
    print(f"Tokens: {result['tokens']}")
    print(f"Cost: ${result['cost']}")
    print(f"\nFeedback:\n{result['feedback']}")
    
    # Example 2: Grade math
    math_sample = """
Solve: ∫(2x + 3)dx from 0 to 5

Solution:
= [x² + 3x] from 0 to 5
= (25 + 15) - (0)
= 40
"""
    
    print("\n" + "=" * 60)
    print("Example 2: Grading math")
    print("=" * 60)
    result = autograde_text(math_sample, content_type="math")
    print(f"Type: {result['detected_type']}")
    print(f"Grade: {result['grade']}/100")
    print(f"Tokens: {result['tokens']}")
    print(f"Cost: ${result['cost']}")
    print(f"\nFeedback:\n{result['feedback']}")
    
    print("\n" + "=" * 60)
    print("SUPPORTED FILE FORMATS:")
    print("=" * 60)
    print("✅ PDF files (.pdf) - Text extraction")
    print("✅ Word documents (.docx) - Text extraction")
    print("✅ Python files (.py) - Direct text")
    print("✅ Text files (.txt, .java, .cpp, .js) - Direct text")
    print("\n❌ Images (.png, .jpg) - NOT SUPPORTED (removed OCR)")
    print("=" * 60)

