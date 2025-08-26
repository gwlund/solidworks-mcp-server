#!/usr/bin/env python3
"""
Update Claude Desktop Configuration with API Key

This script reads the API key from .env file and updates the Claude Desktop configuration.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional

def get_claude_desktop_config_path() -> Path:
    """Get the Claude Desktop configuration file path for the current platform."""
    if sys.platform == "win32":
        # Windows
        config_path = Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        # Linux
        config_path = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    
    return config_path

def read_env_file() -> Optional[str]:
    """Read the API key from the .env file."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return None
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract API key using regex
        match = re.search(r'ANTHROPIC_API_KEY=(.+)', content)
        if match:
            api_key = match.group(1).strip()
            # Remove any trailing comments or whitespace
            api_key = re.sub(r'\s*#.*$', '', api_key).strip()
            return api_key
        else:
            print("❌ ANTHROPIC_API_KEY not found in .env file")
            return None
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return None

def update_claude_config(api_key: str) -> bool:
    """Update the Claude Desktop configuration with the API key."""
    config_path = get_claude_desktop_config_path()
    
    if not config_path.exists():
        print(f"❌ Claude Desktop config not found at: {config_path}")
        return False
    
    try:
        # Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Update the API key
        if "mcpServers" in config and "solidworks-mcp-server" in config["mcpServers"]:
            config["mcpServers"]["solidworks-mcp-server"]["env"]["ANTHROPIC_API_KEY"] = api_key
            print("✓ Updated API key in Claude Desktop configuration")
        else:
            print("❌ SolidWorks MCP server configuration not found")
            return False
        
        # Save updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Configuration saved to: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating configuration: {e}")
        return False

def verify_config() -> bool:
    """Verify the configuration was updated correctly."""
    config_path = get_claude_desktop_config_path()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config["mcpServers"]["solidworks-mcp-server"]["env"]["ANTHROPIC_API_KEY"]
        
        if api_key.startswith("sk-ant-api03-"):
            print("✅ API key verified - configuration is ready!")
            return True
        else:
            print("❌ API key format appears incorrect")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying configuration: {e}")
        return False

def main():
    """Main function to update the configuration."""
    print("SolidWorks MCP Server - Claude Desktop API Key Update")
    print("=" * 55)
    
    # Read API key from .env
    print("Reading API key from .env file...")
    api_key = read_env_file()
    
    if not api_key:
        print("❌ Failed to read API key from .env file")
        return False
    
    print(f"✓ Found API key: {api_key[:20]}...")
    
    # Update Claude Desktop config
    print("\nUpdating Claude Desktop configuration...")
    if not update_claude_config(api_key):
        print("❌ Failed to update Claude Desktop configuration")
        return False
    
    # Verify the update
    print("\nVerifying configuration...")
    if not verify_config():
        print("❌ Configuration verification failed")
        return False
    
    print("\n" + "=" * 55)
    print("🎉 API Key Update Complete!")
    print("=" * 55)
    
    print("\n📋 Next Steps:")
    print("1. Restart Claude Desktop")
    print("2. Test the SolidWorks MCP server")
    print("3. Try asking: 'What SolidWorks tools are available?'")
    
    print("\n🚀 Your SolidWorks MCP server is now ready to use!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
