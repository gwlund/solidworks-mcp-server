#!/usr/bin/env python3
"""
Update Claude Model Configuration

This script updates the Claude Desktop configuration to use a more capable Claude model.
"""

import json
import sys
from pathlib import Path

def get_claude_desktop_config_path():
    """Get the Claude Desktop configuration file path."""
    if sys.platform == "win32":
        config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "darwin":
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    else:
        config_path = Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    
    return config_path

def update_model_config(new_model: str, max_tokens: int = 4000):
    """Update the Claude model configuration."""
    config_path = get_claude_desktop_config_path()
    
    if not config_path.exists():
        print(f"❌ Claude Desktop config not found at: {config_path}")
        return False
    
    try:
        # Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Update the model and tokens
        if "mcpServers" in config and "solidworks-mcp-server" in config["mcpServers"]:
            config["mcpServers"]["solidworks-mcp-server"]["env"]["CLAUDE_MODEL"] = new_model
            config["mcpServers"]["solidworks-mcp-server"]["env"]["CLAUDE_MAX_TOKENS"] = str(max_tokens)
            print(f"✓ Updated model to: {new_model}")
            print(f"✓ Updated max tokens to: {max_tokens}")
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

def main():
    """Main function to update the model."""
    print("Claude Model Configuration Update")
    print("=" * 40)
    
    print("\nAvailable Claude Models (from least to most capable):")
    print("1. claude-3-haiku-20240307 (current) - Fastest, most cost-effective")
    print("2. claude-3-sonnet-20240229 - Balanced performance and cost")
    print("3. claude-3-opus-20240229 - Most capable, highest cost")
    
    print("\nRecommended for SolidWorks CAD operations:")
    print("• claude-3-sonnet-20240229 - Best balance for CAD analysis and complex operations")
    
    # Update to Claude 3 Sonnet (recommended for CAD work)
    new_model = "claude-3-sonnet-20240229"
    max_tokens = 4000  # Increased for more detailed responses
    
    print(f"\nUpdating to: {new_model}")
    print(f"Max tokens: {max_tokens}")
    
    if update_model_config(new_model, max_tokens):
        print("\n" + "=" * 40)
        print("🎉 Model Update Complete!")
        print("=" * 40)
        
        print(f"\n✅ Updated to: {new_model}")
        print(f"✅ Max tokens: {max_tokens}")
        
        print("\n📋 Next Steps:")
        print("1. Restart Claude Desktop")
        print("2. Test with: 'What SolidWorks tools are available?'")
        print("3. Try complex CAD operations for better results")
        
        print("\n💡 Benefits of Claude 3 Sonnet:")
        print("• Better understanding of CAD concepts")
        print("• More detailed analysis of SolidWorks files")
        print("• Improved troubleshooting capabilities")
        print("• Enhanced AI-powered CAD insights")
        
        return True
    else:
        print("❌ Failed to update model configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
