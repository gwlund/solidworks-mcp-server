#!/usr/bin/env python3
"""
Test MCP Server Connection

This script tests if the MCP server can start and respond correctly.
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

def test_server_startup():
    """Test if the server can start without errors."""
    print("Testing MCP server startup...")
    
    try:
        # Start the server in a subprocess
        process = subprocess.Popen(
            [sys.executable, "src/main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a few seconds for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Server started successfully")
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_configuration():
    """Test if the configuration is valid."""
    print("\nTesting configuration...")
    
    try:
        # Test if main.py exists
        main_py = Path("src/main.py")
        if not main_py.exists():
            print("❌ src/main.py not found")
            return False
        
        # Test if Python can import the modules
        result = subprocess.run([
            sys.executable, "-c", 
            "import sys; sys.path.append('src'); from config import Config; print('Configuration module imported successfully')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Configuration is valid")
            return True
        else:
            print(f"❌ Configuration error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def test_dependencies():
    """Test if all dependencies are available."""
    print("\nTesting dependencies...")
    
    required_modules = [
        "mcp",
        "anthropic", 
        "dotenv",
        "pydantic"
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == "dotenv":
                __import__("dotenv")
            else:
                __import__(module.replace("-", "_"))
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {missing_modules}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def main():
    """Main test function."""
    print("SolidWorks MCP Server - Connection Test")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration),
        ("Server Startup", test_server_startup),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST RESULTS SUMMARY")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your MCP server should work with Claude Desktop.")
        print("\nNext steps:")
        print("1. Restart Claude Desktop")
        print("2. Test with: 'What SolidWorks tools are available?'")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before using with Claude Desktop.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
