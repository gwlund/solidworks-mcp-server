#!/usr/bin/env python3
"""
Claude Desktop MCP Server Installer

This script helps install the SolidWorks MCP Server configuration in Claude Desktop.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Optional

def get_claude_desktop_config_path() -> Optional[Path]:
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

def create_config_directory(config_path: Path) -> bool:
    """Create the configuration directory if it doesn't exist."""
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating config directory: {e}")
        return False

def backup_existing_config(config_path: Path) -> bool:
    """Backup existing Claude Desktop configuration if it exists."""
    if config_path.exists():
        backup_path = config_path.with_suffix('.json.backup')
        try:
            shutil.copy2(config_path, backup_path)
            print(f"✓ Backed up existing config to: {backup_path}")
            return True
        except Exception as e:
            print(f"Warning: Could not backup existing config: {e}")
            return False
    return True

def load_current_config(config_path: Path) -> dict:
    """Load existing Claude Desktop configuration or create new one."""
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    config = json.loads(content)
                    print("✓ Loaded existing Claude Desktop configuration")
                    return config
                else:
                    print("✓ Existing config is empty, creating new one")
        except Exception as e:
            print(f"Warning: Could not load existing config: {e}")
    
    # Create new configuration
    config = {"mcpServers": {}}
    print("✓ Created new Claude Desktop configuration")
    return config

def get_project_paths() -> tuple[str, str]:
    """Get the current project paths."""
    current_dir = Path.cwd()
    python_path = "python"  # Use system Python
    
    # Get the main.py path
    main_py_path = current_dir / "src" / "main.py"
    
    if not main_py_path.exists():
        raise FileNotFoundError(f"Could not find src/main.py at {main_py_path}")
    
    return str(python_path), str(main_py_path)

def create_solidworks_config(python_path: str, main_py_path: str) -> dict:
    """Create the SolidWorks MCP server configuration."""
    return {
        "command": python_path,
        "args": [main_py_path],
        "env": {
            "ANTHROPIC_API_KEY": "your-anthropic-api-key-here",
            "SOLIDWORKS_API_KEY": "your-solidworks-api-key-here",
            "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS",
            "SOLIDWORKS_VERSION": "2025",
            "SOLIDWORKS_VISIBLE": "false",
            "CLAUDE_MODEL": "claude-3-haiku-20240307",
            "CLAUDE_MAX_TOKENS": "1000",
            "CLAUDE_TEMPERATURE": "0.7",
            "CLAUDE_TEMP_CATEGORIZATION": "0.3",
            "CLAUDE_TEMP_RESPONSE_GENERATION": "0.7",
            "CLAUDE_TEMP_SUMMARIZATION": "0.4",
            "CLAUDE_TEMP_ACTION_EXTRACTION": "0.2",
            "DEFAULT_EXPORT_FORMAT": "STEP",
            "SOLIDWORKS_TIMEOUT": "30",
            "SOLIDWORKS_RETRY_ATTEMPTS": "3",
            "SOLIDWORKS_BATCH_SIZE": "10",
            "MAX_CONCURRENT_OPERATIONS": "5",
            "CACHE_TTL_SECONDS": "300",
            "MAX_FILE_SIZE_MB": "100",
            "ENABLE_AUDIT_LOGGING": "true",
            "LOG_LEVEL": "INFO",
            "DEBUG_MODE": "false"
        }
    }

def save_config(config: dict, config_path: Path) -> bool:
    """Save the configuration to Claude Desktop config file."""
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved configuration to: {config_path}")
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False

def print_instructions(config_path: Path):
    """Print installation instructions."""
    print("\n" + "=" * 60)
    print("CLAUDE DESKTOP MCP SERVER INSTALLATION")
    print("=" * 60)
    
    print(f"\n✅ Configuration installed at: {config_path}")
    
    print("\n📋 Next Steps:")
    print("1. Update your Anthropic API key in the configuration file")
    print("2. Restart Claude Desktop")
    print("3. Check that the SolidWorks MCP server appears in your tools")
    
    print("\n🔧 To update your API key:")
    print(f"   Edit: {config_path}")
    print("   Replace 'your-anthropic-api-key-here' with your actual API key")
    
    print("\n🚀 Test the installation:")
    print("   - Open Claude Desktop")
    print("   - Try asking: 'What SolidWorks tools are available?'")
    print("   - Or: 'Validate my SolidWorks installation'")
    
    print("\n📁 Configuration details:")
    print(f"   - Config file: {config_path}")
    print(f"   - Python path: {sys.executable}")
    print(f"   - MCP server: {Path.cwd() / 'src' / 'main.py'}")
    
    print("\n" + "=" * 60)

def main():
    """Main installation function."""
    print("SolidWorks MCP Server - Claude Desktop Installer")
    print("=" * 50)
    
    try:
        # Get Claude Desktop config path
        config_path = get_claude_desktop_config_path()
        print(f"Claude Desktop config path: {config_path}")
        
        # Create config directory
        if not create_config_directory(config_path):
            print("❌ Failed to create configuration directory")
            return False
        
        # Backup existing config
        backup_existing_config(config_path)
        
        # Load current config
        config = load_current_config(config_path)
        
        # Get project paths
        python_path, main_py_path = get_project_paths()
        print(f"Python path: {python_path}")
        print(f"MCP server path: {main_py_path}")
        
        # Create SolidWorks configuration
        solidworks_config = create_solidworks_config(python_path, main_py_path)
        
        # Ensure mcpServers exists in config
        if "mcpServers" not in config:
            config["mcpServers"] = {}
        
        # Add to existing config
        config["mcpServers"]["solidworks-mcp-server"] = solidworks_config
        
        # Save configuration
        if not save_config(config, config_path):
            print("❌ Failed to save configuration")
            return False
        
        # Print instructions
        print_instructions(config_path)
        
        print("\n🎉 Installation completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
