#!/usr/bin/env python3
"""
Test script to verify configuration loading without SolidWorks installed.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_config_loading():
    """Test configuration loading with environment variables."""
    print("🧪 Testing Configuration Loading...")
    
    # Set test environment variables
    test_env = {
        "ANTHROPIC_API_KEY": "test_anthropic_key_for_testing",
        "SOLIDWORKS_API_KEY": "test_solidworks_key",
        "SOLIDWORKS_INSTALL_PATH": "/Applications/SOLIDWORKS",
        "SOLIDWORKS_VERSION": "2025",
        "SOLIDWORKS_VISIBLE": "false",
        "CLAUDE_MODEL": "claude-3-haiku-20240307",
        "CLAUDE_MAX_TOKENS": "1000",
        "CLAUDE_TEMPERATURE": "0.7",
        "DEFAULT_EXPORT_FORMAT": "STEP",
        "LOG_LEVEL": "DEBUG",
        "DEBUG_MODE": "true"
    }
    
    # Set environment variables
    for key, value in test_env.items():
        os.environ[key] = value
    
    try:
        from config import Config
        
        # Test configuration loading
        config = Config.from_environment()
        
        print("✅ Configuration loaded successfully!")
        print(f"   - Anthropic API Key: {config.anthropic_api_key[:20]}...")
        print(f"   - SolidWorks Version: {config.solidworks_version}")
        print(f"   - Claude Model: {config.claude_model}")
        print(f"   - Debug Mode: {config.debug_mode}")
        print(f"   - Log Level: {config.log_level}")
        print(f"   - Max Concurrent Operations: {config.max_concurrent_operations}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_server_initialization():
    """Test server initialization without starting it."""
    print("\n🧪 Testing Server Initialization...")
    
    try:
        from config import Config
        from server import MCPServer
        
        # Load configuration
        config = Config.from_environment()
        
        # Initialize server (but don't start it)
        server = MCPServer(config=config)
        
        print("✅ MCP Server initialized successfully!")
        print(f"   - Server has SolidWorks tools: {server._solidworks_tools is not None}")
        print(f"   - Server has CAD resources: {server._cad_resources is not None}")
        print(f"   - Server has SolidWorks prompts: {server._solidworks_prompts is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Server initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tools_functionality():
    """Test tools functionality without SolidWorks."""
    print("\n🧪 Testing Tools Functionality...")
    
    try:
        from tools.solidworks_tools import SolidWorksTools
        import asyncio
        
        tools = SolidWorksTools()
        
        # Test list_tools
        tools_list = asyncio.run(tools.list_tools())
        print(f"✅ Tools list loaded: {len(tools_list)} tools available")
        for tool in tools_list:
            print(f"   - {tool.name}: {tool.description}")
        
        # Test a simple tool call (this should work even without SolidWorks)
        result = asyncio.run(tools.get_supported_formats("all"))
        print(f"✅ Get supported formats: {result['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tools functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resources_functionality():
    """Test resources functionality."""
    print("\n🧪 Testing Resources Functionality...")
    
    try:
        from resources.cad_resources import CADResources
        import asyncio
        
        resources = CADResources()
        
        # Test list_resources
        resources_list = asyncio.run(resources.list_resources())
        print(f"✅ Resources list loaded: {len(resources_list)} resources available")
        for resource in resources_list:
            print(f"   - {resource.name}: {resource.description}")
        
        # Test reading a resource
        system_status = asyncio.run(resources.read_resource("cad://system/status"))
        print(f"✅ System status resource: {len(system_status)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Resources functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prompts_functionality():
    """Test prompts functionality."""
    print("\n🧪 Testing Prompts Functionality...")
    
    try:
        from prompts.cad_prompts import SolidWorksPrompts
        import asyncio
        
        prompts = SolidWorksPrompts()
        
        # Test list_prompts
        prompts_list = asyncio.run(prompts.list_prompts())
        print(f"✅ Prompts list loaded: {len(prompts_list)} prompts available")
        for prompt in prompts_list:
            print(f"   - {prompt.name}: {prompt.description}")
        
        # Test getting a prompt
        test_prompt = asyncio.run(prompts.get_prompt(
            "analyze_cad_file", 
            {"file_path": "/test/file.sldprt", "analysis_focus": "design"}
        ))
        print(f"✅ Analyze CAD file prompt: {len(test_prompt)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompts functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 SolidWorks MCP Server - Test Suite")
    print("=" * 50)
    
    tests = [
        test_config_loading,
        test_server_initialization,
        test_tools_functionality,
        test_resources_functionality,
        test_prompts_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The MCP server should work on a computer with SolidWorks.")
        print("\n📋 Next steps:")
        print("   1. Copy this code to a computer with SolidWorks installed")
        print("   2. Update .env with real ANTHROPIC_API_KEY")
        print("   3. Set correct SOLIDWORKS_INSTALL_PATH")
        print("   4. Run: python src/main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before deploying.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
