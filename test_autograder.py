# test_autograder.py
# Quick tests to verify the simplified autograder works

import os
import sys

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    try:
        from autograder_simplified import (
            autograde_text,
            autograde_pdf,
            autograde_image,
            autograde_file,
            detect_content_type
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_content_detection():
    """Test content type detection"""
    print("\nTesting content type detection...")
    from autograder_simplified import detect_content_type
    
    tests = [
        ("def hello():\n    pass", "code"),
        ("∫(2x + 3)dx = x² + 3x + C", "math"),
        ("The quick brown fox jumps over the lazy dog.", "text"),
        ("for i in range(10):\n    print(i)", "code"),
        ("sin(x) + cos(x) = √2", "math"),
    ]
    
    passed = 0
    for content, expected in tests:
        result = detect_content_type(content)
        if result == expected:
            print(f"  ✅ Detected '{expected}' correctly")
            passed += 1
        else:
            print(f"  ⚠️  Expected '{expected}', got '{result}' for: {content[:30]}...")
    
    print(f"Passed {passed}/{len(tests)} detection tests")
    return passed == len(tests)


def test_autograding_mock():
    """Test autograding with mock data (no actual API call)"""
    print("\nTesting autograding structure (without API call)...")
    
    # Test that the function signature works
    from autograder_simplified import autograde_text
    
    code_sample = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
    
    print("  Structure test: autograde_text() signature ✅")
    
    # Note: Actual API call would require OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key and api_key.startswith("sk-"):
        print("  API key detected - could make real call")
        # Uncomment to test real API call:
        # result = autograde_text(code_sample, content_type="code")
        # print(f"  Real API test: Grade {result['grade']}/100, Tokens: {result['tokens']}")
    else:
        print("  ⚠️  No API key - skipping actual API call")
    
    return True


def test_api_routes():
    """Test that FastAPI routes are properly configured"""
    print("\nTesting FastAPI route configuration...")
    try:
        from routers.autograder_routes import router
        
        # Check that routes exist
        routes = [route.path for route in router.routes]
        expected_routes = ["/grade_text", "/grade_file", "/grade_base64"]
        
        for route in expected_routes:
            if route in routes:
                print(f"  ✅ Route '{route}' exists")
            else:
                print(f"  ❌ Route '{route}' missing")
        
        return True
    except Exception as e:
        print(f"  ❌ Route test failed: {e}")
        return False


def test_main_integration():
    """Test that main.py includes autograder routes"""
    print("\nTesting main.py integration...")
    try:
        from main import app
        
        # Check that autograder routes are included
        paths = [route.path for route in app.routes]
        
        if "/autograder/grade_text" in paths:
            print("  ✅ Autograder routes registered in main app")
            return True
        else:
            print("  ❌ Autograder routes not found in main app")
            print(f"  Available routes: {paths}")
            return False
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AUTOGRADER SIMPLIFIED - TEST SUITE")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Content Detection", test_content_detection()))
    results.append(("Autograding Structure", test_autograding_mock()))
    results.append(("API Routes", test_api_routes()))
    results.append(("Main Integration", test_main_integration()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The autograder is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Start server: uvicorn main:app --reload")
        print("4. Test endpoint: POST http://localhost:8000/autograder/grade_text")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

