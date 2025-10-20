# Complete Testing Guide

## Step-by-Step: Open Site and Test Fully

### Step 1: Set Your OpenAI API Key

**Open PowerShell in the Token-Counter folder and run:**

```powershell
# Set your OpenAI API key (replace with your actual key)
$env:OPENAI_API_KEY="sk-your-actual-key-here"

# Verify it's set
echo $env:OPENAI_API_KEY
```

**Don't have a key yet?**
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

---

### Step 2: Start the Server

**Option A: Using the startup script (Recommended)**
```powershell
.\start_server.ps1
```

**Option B: Manually**
```powershell
uvicorn main:app --reload
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

### Step 3: Open the Interactive API Documentation

**Open your web browser and go to:**

🌐 **http://localhost:8000/docs**

You'll see a beautiful Swagger UI interface with all API endpoints!

---

## 🧪 Full Testing Walkthrough

### Test 1: Check if Server is Running

**In browser, go to:** http://localhost:8000

**Expected response:**
```json
{
  "message": "Token tracking & autograder is up ✨"
}
```

✅ Server is running!

---

### Test 2: Create a Test User

**In Swagger UI (http://localhost:8000/docs):**

1. Scroll to **`POST /tokens/bootstrap`**
2. Click **"Try it out"**
3. Fill in:
   - `user_id`: `alice`
   - `name`: `Alice Smith`
   - `role`: `student`
   - `token_limit`: `100000`
4. Click **"Execute"**

**Expected response:**
```json
{
  "message": "ok",
  "user": {
    "id": "alice",
    "name": "Alice Smith",
    "role": "student",
    "token_limit": 100000,
    "token_used": 0
  }
}
```

✅ User created!

---

### Test 3: Grade Code (Text Input)

**In Swagger UI:**

1. Scroll to **`POST /autograder/grade_text`**
2. Click **"Try it out"**
3. Paste this JSON:

```json
{
  "user_id": "alice",
  "content": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial(5))",
  "content_type": "code"
}
```

4. Click **"Execute"**

**Expected response:**
```json
{
  "detected_type": "code",
  "feedback": "The code correctly implements factorial using recursion. However, it lacks input validation and could cause stack overflow for large inputs. Consider adding error handling.\n\nFINAL GRADE: 85/100",
  "grade": 85,
  "user_id": "alice"
}
```

✅ Code grading works!

---

### Test 4: Grade Math Problem

**In Swagger UI:**

1. Stay on **`POST /autograder/grade_text`**
2. Click **"Try it out"** (if not already)
3. Paste this JSON:

```json
{
  "user_id": "alice",
  "content": "Solve: ∫(2x + 3)dx from 0 to 5\n\nSolution:\n= [x² + 3x] from 0 to 5\n= (25 + 15) - (0)\n= 40",
  "content_type": "math"
}
```

4. Click **"Execute"**

**Expected response:**
```json
{
  "detected_type": "math",
  "feedback": "The integration is correct and the calculation is accurate. Good step-by-step work. Could benefit from showing the antiderivative formula more clearly.\n\nFINAL GRADE: 90/100",
  "grade": 90,
  "user_id": "alice"
}
```

✅ Math grading works!

---

### Test 5: Upload and Grade a File (PDF or Image)

**In Swagger UI:**

1. Scroll to **`POST /autograder/grade_file`**
2. Click **"Try it out"**
3. Fill in:
   - `user_id`: `alice`
4. Click **"Choose File"** and select a file:
   - PDF document
   - PNG/JPG image (will use OCR)
   - .py/.java/.txt file
5. Click **"Execute"**

**Expected response:**
```json
{
  "detected_type": "code",
  "feedback": "[AI-generated feedback based on file content]\n\nFINAL GRADE: 87/100",
  "grade": 87,
  "user_id": "alice",
  "filename": "your-file-name.pdf"
}
```

✅ File upload and grading works!

---

### Test 6: Check Token Usage

**In Swagger UI:**

1. Scroll to **`GET /tokens/usage/{user_id}`**
2. Click **"Try it out"**
3. Enter `user_id`: `alice`
4. Click **"Execute"**

**Expected response:**
```json
{
  "user": {
    "id": "alice",
    "name": "Alice Smith",
    "role": "student",
    "token_limit": 100000,
    "token_used": 1234
  },
  "remaining_tokens": 98766
}
```

✅ Token tracking works!

---

### Test 7: View Usage Logs

**In Swagger UI:**

1. Scroll to **`GET /tokens/logs/{user_id}`**
2. Click **"Try it out"**
3. Enter `user_id`: `alice`
4. Click **"Execute"**

**Expected response:**
```json
[
  {
    "id": 1,
    "user_id": "alice",
    "request_type": "autograde",
    "model": "gpt-4o",
    "tokens_used": 245,
    "cost_usd": 0.003675,
    "timestamp": "2025-10-16T16:23:37.000000"
  },
  {
    "id": 2,
    "user_id": "alice",
    "request_type": "autograde",
    "model": "gpt-4o",
    "tokens_used": 198,
    "cost_usd": 0.00297,
    "timestamp": "2025-10-16T16:24:15.000000"
  }
]
```

✅ Usage logging works!

---

## 🎨 Alternative: Test with Code

If you prefer testing with Python code instead of the web interface:

```python
import requests

BASE_URL = "http://localhost:8000"

# Test 1: Check server
response = requests.get(f"{BASE_URL}/")
print("Server:", response.json())

# Test 2: Create user
response = requests.post(f"{BASE_URL}/tokens/bootstrap?user_id=bob&name=Bob&token_limit=50000")
print("User created:", response.json())

# Test 3: Grade code
response = requests.post(f"{BASE_URL}/autograder/grade_text", json={
    "user_id": "bob",
    "content": "def hello():\n    print('Hello, World!')",
    "content_type": "code"
})
result = response.json()
print(f"Grade: {result['grade']}/100")
print(f"Feedback: {result['feedback']}")

# Test 4: Check usage
response = requests.get(f"{BASE_URL}/tokens/usage/bob")
print("Token usage:", response.json())
```

Save as `test_api.py` and run:
```powershell
python test_api.py
```

---

## 🖼️ Test Your Original Image

Since you already tried uploading an image earlier:

1. Go to: http://localhost:8000/docs
2. Click **`POST /autograder/grade_file`**
3. Click **"Try it out"**
4. Enter `user_id`: `alice`
5. Upload your image: `LANGAtestingforimagerecognition.png`
6. Click **"Execute"**

**This time you should get actual AI feedback instead of an error!**

---

## 📊 What to Look For

### Success Indicators

✅ **Server starts without errors**
✅ **Can access http://localhost:8000/docs**
✅ **All endpoints show up in Swagger UI**
✅ **Can create users**
✅ **Gets actual AI feedback (not error messages)**
✅ **Grades are extracted (numbers 0-100)**
✅ **Token usage is tracked**
✅ **Logs are recorded**

### Failure Indicators

❌ **"AI feedback failed: Expecting value..."** → API key not set
❌ **"ModuleNotFoundError"** → Run `pip install -r requirements.txt`
❌ **"AuthenticationError"** → Invalid API key
❌ **"Rate limit exceeded"** → Too many requests, wait
❌ **"Insufficient quota"** → No OpenAI credits

---

## 🎯 Complete Test Checklist

- [ ] Server starts successfully
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:8000/docs
- [ ] Can create a test user
- [ ] Can grade text/code
- [ ] Can grade math
- [ ] Can upload and grade files
- [ ] Can check token usage
- [ ] Can view usage logs
- [ ] Grades are numbers (not null)
- [ ] Feedback is meaningful (not error messages)
- [ ] Token counts increase after grading

---

## 🔍 Debugging Tips

### Check Server Logs

Look at the terminal where uvicorn is running. You should see:

```
INFO:     127.0.0.1:xxxxx - "POST /autograder/grade_text HTTP/1.1" 200 OK
```

If you see errors, they'll show up here.

### Check tokens.json

Open `tokens.json` in the Token-Counter folder to see stored data:

```json
{
  "users": {
    "alice": {
      "id": "alice",
      "name": "Alice Smith",
      "token_limit": 100000,
      "token_used": 1234
    }
  },
  "logs": [
    {
      "id": 1,
      "user_id": "alice",
      "tokens_used": 245,
      ...
    }
  ]
}
```

### Enable Debug Mode

Edit `start_server.ps1` and change the last line to:
```powershell
uvicorn main:app --reload --log-level debug
```

---

## 🎉 You're All Set!

Once all tests pass, your autograder is fully functional!

**Key URLs:**
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

**Happy testing! 🚀**

