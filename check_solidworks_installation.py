#!/usr/bin/env python3
"""
SolidWorks Installation Checker

This script checks your SolidWorks installation and provides guidance for testing
the MCP server with your specific SolidWorks version.
"""

import os
import sys
import subprocess
import winreg
from pathlib import Path
from typing import Optional, Dict, Any

def check_solidworks_registry() -> Optional[Dict[str, Any]]:
    """Check SolidWorks installation in Windows registry."""
    print("Checking SolidWorks installation in registry...")
    
    solidworks_versions = []
    
    # Check common SolidWorks registry keys
    registry_paths = [
        r"SOFTWARE\SolidWorks\SolidWorks",
        r"SOFTWARE\WOW6432Node\SolidWorks\SolidWorks",
        r"SOFTWARE\SolidWorks Corp\SolidWorks",
        r"SOFTWARE\WOW6432Node\SolidWorks Corp\SolidWorks"
    ]
    
    for registry_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                # Get all subkeys (versions)
                i = 0
                while True:
                    try:
                        version_key = winreg.EnumKey(key, i)
                        solidworks_versions.append(version_key)
                        i += 1
                    except WindowsError:
                        break
        except WindowsError:
            continue
    
    if solidworks_versions:
        print(f"✓ Found SolidWorks versions in registry: {solidworks_versions}")
        return {"versions": solidworks_versions, "source": "registry"}
    else:
        print("✗ No SolidWorks versions found in registry")
        return None

def check_solidworks_installation_path() -> Optional[Dict[str, Any]]:
    """Check common SolidWorks installation paths."""
    print("Checking SolidWorks installation paths...")
    
    common_paths = [
        r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS",
        r"C:\Program Files\SolidWorks Corp\SolidWorks",
        r"C:\Program Files (x86)\SOLIDWORKS Corp\SOLIDWORKS",
        r"C:\Program Files (x86)\SolidWorks Corp\SolidWorks"
    ]
    
    for path in common_paths:
        if Path(path).exists():
            print(f"✓ Found SolidWorks installation at: {path}")
            
            # Check for executable
            exe_path = Path(path) / "SLDWORKS.exe"
            if exe_path.exists():
                print(f"✓ Found SolidWorks executable: {exe_path}")
                return {"path": path, "executable": str(exe_path)}
            else:
                print(f"⚠️  Installation found but executable not found at: {exe_path}")
    
    print("✗ No SolidWorks installation found in common paths")
    return None

def check_solidworks_running() -> bool:
    """Check if SolidWorks is currently running."""
    print("Checking if SolidWorks is currently running...")
    
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq SLDWORKS.exe"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if "SLDWORKS.exe" in result.stdout:
            print("✓ SolidWorks is currently running")
            return True
        else:
            print("ℹ️  SolidWorks is not currently running")
            return False
            
    except subprocess.CalledProcessError:
        print("ℹ️  Could not check if SolidWorks is running")
        return False

def check_python_dependencies() -> Dict[str, bool]:
    """Check if required Python dependencies are installed."""
    print("Checking Python dependencies...")
    
    required_packages = [
        "mcp",
        "anthropic", 
        "python-dotenv",
        "pydantic"
    ]
    
    results = {}
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package} is installed")
            results[package] = True
        except ImportError:
            print(f"✗ {package} is not installed")
            results[package] = False
    
    return results

def create_env_template() -> None:
    """Create a .env template file."""
    print("Creating .env template file...")
    
    env_content = """# SolidWorks MCP Server Environment Configuration
# Update these values with your actual configuration

# REQUIRED: Anthropic Claude API Key
# Get your API key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# SolidWorks Configuration
# Update the path to match your SolidWorks installation
SOLIDWORKS_INSTALL_PATH=C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS
SOLIDWORKS_VERSION=2025
SOLIDWORKS_VISIBLE=false
SOLIDWORKS_TIMEOUT=30
SOLIDWORKS_RETRY_ATTEMPTS=3
SOLIDWORKS_BATCH_SIZE=10

# Claude AI Configuration
CLAUDE_MODEL=claude-3-haiku-20240307
CLAUDE_MAX_TOKENS=1000
CLAUDE_TEMPERATURE=0.7

# Claude Temperature Settings
CLAUDE_TEMP_CATEGORIZATION=0.3
CLAUDE_TEMP_RESPONSE_GENERATION=0.7
CLAUDE_TEMP_SUMMARIZATION=0.4
CLAUDE_TEMP_ACTION_EXTRACTION=0.2

# File Export Configuration
DEFAULT_EXPORT_FORMAT=STEP

# Logging Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false

# Performance Configuration
MAX_CONCURRENT_OPERATIONS=5
CACHE_TTL_SECONDS=300
MAX_FILE_SIZE_MB=100

# Security Configuration
ENABLE_AUDIT_LOGGING=true
MAX_LOG_FILE_SIZE_MB=50
LOG_RETENTION_DAYS=30
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✓ Created .env file with template values")

def main():
    """Main function to check SolidWorks installation."""
    print("SolidWorks MCP Server - Installation Checker")
    print("=" * 50)
    
    # Check registry
    registry_info = check_solidworks_registry()
    
    # Check installation paths
    path_info = check_solidworks_installation_path()
    
    # Check if SolidWorks is running
    is_running = check_solidworks_running()
    
    # Check Python dependencies
    print("\n" + "=" * 50)
    deps = check_python_dependencies()
    
    # Create .env template if it doesn't exist
    if not Path(".env").exists():
        print("\n" + "=" * 50)
        create_env_template()
    
    # Summary and recommendations
    print("\n" + "=" * 50)
    print("SUMMARY AND RECOMMENDATIONS")
    print("=" * 50)
    
    if registry_info or path_info:
        print("✓ SolidWorks installation detected")
        
        if registry_info:
            print(f"  - Registry versions: {registry_info['versions']}")
        
        if path_info:
            print(f"  - Installation path: {path_info['path']}")
            print(f"  - Executable: {path_info['executable']}")
        
        if is_running:
            print("  - SolidWorks is currently running")
        else:
            print("  - SolidWorks is not running (this is normal)")
        
        print("\nNext steps:")
        print("1. Update the .env file with your Anthropic API key")
        print("2. Update SOLIDWORKS_INSTALL_PATH if needed")
        print("3. Update SOLIDWORKS_VERSION to match your installation")
        print("4. Run: python test_solidworks_integration.py")
        
    else:
        print("✗ SolidWorks installation not found")
        print("\nPlease ensure SolidWorks is properly installed and try again.")
    
    # Check dependencies
    missing_deps = [pkg for pkg, installed in deps.items() if not installed]
    if missing_deps:
        print(f"\nMissing dependencies: {missing_deps}")
        print("Install them with: pip install -r requirements.txt")
    else:
        print("\n✓ All required Python dependencies are installed")
    
    print("\n" + "=" * 50)
    print("Ready to test your SolidWorks MCP server!")

if __name__ == "__main__":
    main()
