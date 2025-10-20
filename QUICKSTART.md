# 🚀 Quick Start Guide - Simplified Autograder

## TL;DR

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set OpenAI API key ⚠️ REQUIRED!
$env:OPENAI_API_KEY="sk-your-actual-key-here"
# Get your key from: https://platform.openai.com/api-keys

# 3. Start server
uvicorn main:app --reload

# 4. Test it
curl -X POST "http://localhost:8000/autograder/grade_text" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "content": "def hello(): pass", "content_type": "code"}'
```

> ⚠️ **IMPORTANT**: The autograder will NOT work without a valid OpenAI API key!

---

## 📋 Installation Steps

### Step 1: Install Python Dependencies

```powershell
cd C:\Users\User\Desktop\Token-Counter
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.111.0 uvicorn-0.30.1 openai-1.35.0 ...
```

### Step 2: Install Tesseract OCR (Optional - for image grading)

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`
3. Already configured in code ✅

**Skip if you only need code/text grading (no images)**

### Step 3: Set OpenAI API Key

```powershell
# PowerShell (Windows)
$env:OPENAI_API_KEY="sk-your-actual-key-here"

# Verify it's set
echo $env:OPENAI_API_KEY
```

**Get your key**: https://platform.openai.com/api-keys

---

## ✅ Verify Installation

Run the test suite:

```powershell
python test_autograder.py
```

**Expected output:**
```
============================================================
AUTOGRADER SIMPLIFIED - TEST SUITE
============================================================
✅ PASS - Imports
✅ PASS - Content Detection
✅ PASS - Autograding Structure
✅ PASS - API Routes
✅ PASS - Main Integration

Total: 5/5 tests passed

🎉 All tests passed! The autograder is ready to use.
```

---

## 🚀 Start the Server

```powershell
uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Interactive Docs**: http://localhost:8000/docs

---

## 🧪 Test the Endpoints

### Option 1: Using the Web Interface

1. Open browser: http://localhost:8000/docs
2. Click on `POST /autograder/grade_text`
3. Click "Try it out"
4. Paste this JSON:
```json
{
  "user_id": "alice",
  "content": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
  "content_type": "code"
}
```
5. Click "Execute"

### Option 2: Using curl (PowerShell)

```powershell
# Grade code
curl -X POST "http://localhost:8000/autograder/grade_text" `
  -H "Content-Type: application/json" `
  -d '{\"user_id\": \"alice\", \"content\": \"def hello(): pass\", \"content_type\": \"code\"}'
```

### Option 3: Using Python

```python
import requests

response = requests.post("http://localhost:8000/autograder/grade_text", json={
    "user_id": "alice",
    "content": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
    "content_type": "code"
})

result = response.json()
print(f"Grade: {result['grade']}/100")
print(f"Feedback:\n{result['feedback']}")
```

---

## 📊 Example Responses

### Success Response
```json
{
  "detected_type": "code",
  "feedback": "The code correctly implements factorial using recursion. However, it lacks input validation and could cause stack overflow for large inputs.\n\nFINAL GRADE: 87/100",
  "grade": 87,
  "user_id": "alice"
}
```

### Error Response
```json
{
  "detail": "Missing 'content' field"
}
```

---

## 🎯 Common Use Cases

### 1. Grade Text Code

```python
import requests

code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
"""

response = requests.post("http://localhost:8000/autograder/grade_text", json={
    "user_id": "student_123",
    "content": code,
    "content_type": "code"
})

print(response.json())
```

### 2. Grade Math Problem

```python
math = """
Solve: ∫(2x + 3)dx from 0 to 5

Solution:
= [x² + 3x] from 0 to 5
= (25 + 15) - (0)
= 40
"""

response = requests.post("http://localhost:8000/autograder/grade_text", json={
    "user_id": "student_123",
    "content": math,
    "content_type": "math"
})

print(response.json())
```

### 3. Upload and Grade PDF

```python
with open("student_submission.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/autograder/grade_file",
        data={"user_id": "student_123"},
        files={"file": f}
    )

print(response.json())
```

### 4. Check Token Usage

```python
usage = requests.get("http://localhost:8000/tokens/usage/student_123").json()
print(f"Tokens used: {usage['user']['token_used']}")
print(f"Remaining: {usage['remaining_tokens']}")
```

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```powershell
pip install -r requirements.txt
```

### Problem: "openai.AuthenticationError"

**Solution:**
```powershell
# Set API key
$env:OPENAI_API_KEY="sk-your-key-here"

# Verify
echo $env:OPENAI_API_KEY
```

### Problem: "Form data requires python-multipart"

**Solution:**
```powershell
pip install python-multipart
```

### Problem: "⚠️ OCR extraction failed"

**Solutions:**
1. Install Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Or skip image grading (use text/PDF only)

### Problem: Port 8000 already in use

**Solution:**
```powershell
# Use different port
uvicorn main:app --port 8001
```

---

## 📁 File Locations

```
C:\Users\User\Desktop\Token-Counter\
│
├── main.py                      ← FastAPI app
├── autograder_simplified.py     ← Core autograder
├── routers/
│   └── autograder_routes.py     ← API endpoints
│
├── test_autograder.py           ← Run this to test
├── requirements.txt             ← Install this
│
└── tokens.json                  ← Auto-created (token usage)
```

---

## 🔑 Environment Variables

```powershell
# Required
$env:OPENAI_API_KEY="sk-..."

# Optional
$env:MODEL_NAME="gpt-4o-mini"  # Use cheaper model
```

---

## 📚 Next Steps

1. **Read Full Documentation**: `AUTOGRADER_README.md`
2. **See Comparison**: `COMPARISON.md`
3. **Understand Architecture**: `ARCHITECTURE.md`
4. **Read Summary**: `SUMMARY.md`

---

## 🎓 Production Checklist

Before deploying to production:

- [ ] Set API key as environment variable (not in code)
- [ ] Add rate limiting (prevent abuse)
- [ ] Add input validation (file size limits)
- [ ] Use HTTPS (secure connection)
- [ ] Add logging (track errors)
- [ ] Add monitoring (track performance)
- [ ] Set up backup (tokens.json)
- [ ] Test with real students
- [ ] Document API for students
- [ ] Set token limits per student

---

## 💡 Pro Tips

### Tip 1: Use Cheaper Model for Testing

```python
# In autograder_simplified.py or autograder_routes.py
MODEL_NAME = "gpt-4o-mini"  # Cheaper ($0.15/1M tokens vs $5/1M)
```

### Tip 2: Bootstrap Users First

```python
# Create user before first grading
requests.post("http://localhost:8000/tokens/bootstrap?user_id=alice&token_limit=100000")
```

### Tip 3: Batch Process Submissions

```python
import concurrent.futures

def grade_submission(filename):
    with open(filename, "rb") as f:
        return requests.post(
            "http://localhost:8000/autograder/grade_file",
            data={"user_id": filename.split('.')[0]},
            files={"file": f}
        ).json()

# Grade multiple files in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(grade_submission, ["file1.pdf", "file2.py", "file3.png"])
```

---

## ⚡ Performance

**Typical Response Times:**
- Text grading: 2-3 seconds
- PDF grading: 4-6 seconds
- Image grading: 5-8 seconds

**Throughput:**
- Single worker: ~20 requests/minute
- Multiple workers: ~100 requests/minute

**Cost (OpenAI):**
- Per grading: $0.002 - $0.008
- Per 100 gradings: ~$0.50
- Per 1000 gradings: ~$5.00

---

## 🎯 You're All Set!

Your autograder is now running at:

**API**: http://localhost:8000  
**Docs**: http://localhost:8000/docs  
**Test**: See examples above

**Happy grading! 🎓✨**

---

## 📞 Need Help?

1. Run tests: `python test_autograder.py`
2. Check logs: Look at uvicorn output
3. Read docs: `AUTOGRADER_README.md`
4. Verify API key: `echo $env:OPENAI_API_KEY`

**Common issues are usually:**
- Missing API key ← Set `$env:OPENAI_API_KEY`
- Missing dependencies ← Run `pip install -r requirements.txt`
- Wrong port ← Use `--port 8001`

