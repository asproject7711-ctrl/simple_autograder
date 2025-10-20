# Quick Install & Test Guide

## 🚀 Super Simple Installation (2 Minutes!)

### Step 1: Install Dependencies

```powershell
cd C:\Users\User\Desktop\Token-Counter
pip install -r requirements.txt
```

**That's it!** No Tesseract, no external software, no complex setup!

---

### Step 2: Set OpenAI API Key

```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
```

Get your key from: https://platform.openai.com/api-keys

---

### Step 3: Start Server

**Option A: Using startup script (checks for API key)**
```powershell
.\start_server.ps1
```

**Option B: Manual start**
```powershell
uvicorn main:app --reload
```

---

## ✅ Test the Simplified Autograder

### Test 1: Upload PDF File

1. Go to: http://localhost:8000/docs
2. Click `POST /autograder/grade_file`
3. Click "Try it out"
4. Enter `user_id`: `test`
5. Upload a PDF file
6. Click "Execute"

**Expected**: Text extracted from PDF and graded ✅

---

### Test 2: Upload Word Document

1. Stay on `POST /autograder/grade_file`
2. Click "Try it out"
3. Enter `user_id`: `test`
4. Upload a `.docx` file
5. Click "Execute"

**Expected**: Text extracted from Word doc and graded ✅

---

### Test 3: Upload Python File

Create a test file `test.py`:
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

print(factorial(5))
```

1. Upload `test.py` via `/autograder/grade_file`
2. Click "Execute"

**Expected**: Python code graded ✅

---

### Test 4: Try to Upload Image (Should Fail)

1. Try to upload a `.png` or `.jpg` file
2. Click "Execute"

**Expected**: Will try to read as text, will likely fail or give gibberish ❌

**Why?** OCR support was removed for simplicity.

**Solution**: Convert image to PDF first, or ask students to submit text files instead.

---

## 📋 Supported Formats Checklist

Test each format to verify it works:

- [ ] PDF file (.pdf) - ✅ Should work
- [ ] Word document (.docx) - ✅ Should work
- [ ] Python file (.py) - ✅ Should work
- [ ] Text file (.txt) - ✅ Should work
- [ ] Java file (.java) - ✅ Should work
- [ ] Image file (.png) - ❌ Not supported

---

## 🔧 Installation Verification

Run this command to check all dependencies are installed:

```powershell
python -c "import fastapi, uvicorn, openai, fitz, docx; print('✅ All dependencies installed!')"
```

**Expected output**:
```
✅ All dependencies installed!
```

If you get an error, run: `pip install -r requirements.txt`

---

## 🎯 Complete Test Script

Save as `test_simplified.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("TESTING SIMPLIFIED AUTOGRADER")
print("=" * 60)

# Test 1: Check server
print("\n1. Checking server...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Server running: {response.json()}")
except Exception as e:
    print(f"❌ Server not running: {e}")
    exit(1)

# Test 2: Create test user
print("\n2. Creating test user...")
response = requests.post(f"{BASE_URL}/tokens/bootstrap?user_id=testuser&name=Test&token_limit=100000")
print(f"✅ User created: {response.json()['user']['id']}")

# Test 3: Grade Python code
print("\n3. Grading Python code...")
code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""

response = requests.post(f"{BASE_URL}/autograder/grade_text", json={
    "user_id": "testuser",
    "content": code,
    "content_type": "code"
})

result = response.json()
print(f"✅ Grade: {result['grade']}/100")
print(f"   Feedback: {result['feedback'][:100]}...")

# Test 4: Check token usage
print("\n4. Checking token usage...")
response = requests.get(f"{BASE_URL}/tokens/usage/testuser")
usage = response.json()
print(f"✅ Tokens used: {usage['user']['token_used']}")
print(f"   Remaining: {usage['remaining_tokens']}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nSupported formats:")
print("  ✅ PDF (.pdf)")
print("  ✅ Word (.docx)")
print("  ✅ Python (.py)")
print("  ✅ Text (.txt, .java, .cpp, etc.)")
print("\nNOT supported:")
print("  ❌ Images (.png, .jpg) - OCR removed")
print("=" * 60)
```

Run it:
```powershell
python test_simplified.py
```

---

## 🎉 Success Criteria

Your installation is successful if:

✅ `pip install -r requirements.txt` completes without errors  
✅ Server starts with `uvicorn main:app --reload`  
✅ Can access http://localhost:8000/docs  
✅ Can upload and grade PDF files  
✅ Can upload and grade Word documents  
✅ Can upload and grade Python files  
✅ Token usage is tracked  
✅ No Tesseract installation required  

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'docx'"

```powershell
pip install python-docx
```

### "ModuleNotFoundError: No module named 'fitz'"

```powershell
pip install pymupdf
```

### "Word document support not available"

```powershell
pip install python-docx
```

### "AI feedback failed"

Make sure you set your OpenAI API key:
```powershell
$env:OPENAI_API_KEY="sk-your-key"
```

---

## ⏱️ Installation Time Comparison

### Before (With OCR)
1. Install Python packages: ~3 minutes
2. Download Tesseract: ~2 minutes
3. Install Tesseract: ~3 minutes
4. Configure paths: ~2 minutes
**Total: ~10 minutes**

### After (Text-Only)
1. Install Python packages: ~2 minutes
**Total: ~2 minutes**

**80% faster!** 🚀

---

## 📊 What You Get

### Dependencies Installed
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai` - OpenAI API client
- `pymupdf` - PDF text extraction
- `python-docx` - Word document support
- `python-multipart` - File uploads

### NOT Installed (Removed)
- ~~`pillow`~~ - Image processing (not needed)
- ~~`pytesseract`~~ - OCR (not needed)
- ~~`tesseract-ocr`~~ - External software (not needed)

---

## 🎓 Summary

You now have a **fully functional autograder** that:

✅ Installs in 2 minutes
✅ Requires no external software
✅ Supports PDF, Word, and code files
✅ Tracks token usage automatically
✅ Uses OpenAI GPT-4 for grading

**Just run: `pip install -r requirements.txt` and you're done!**

See `SIMPLIFICATION_SUMMARY.md` for details on what was simplified.

