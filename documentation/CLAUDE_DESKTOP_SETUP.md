# Claude Desktop Configuration for SolidWorks MCP Server

This guide shows you how to configure Claude Desktop to use your SolidWorks MCP server.

## 📍 Configuration File Location

Claude Desktop stores its configuration in different locations depending on your operating system:

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Linux
```
~/.config/Claude/claude_desktop_config.json
```

## 🔧 Setup Instructions

### Step 1: Locate Your Claude Desktop Config

1. **Find the config directory:**
   ```bash
   # macOS
   open ~/Library/Application\ Support/Claude/
   
   # Windows (in PowerShell)
   explorer $env:APPDATA\Claude\
   
   # Linux
   mkdir -p ~/.config/Claude && cd ~/.config/Claude
   ```

2. **Create the config file if it doesn't exist:**
   ```bash
   # macOS/Linux
   touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   New-Item -Path "$env:APPDATA\Claude\claude_desktop_config.json" -ItemType File
   ```

### Step 2: Add SolidWorks MCP Server Configuration

**Option A: Use the template file**
```bash
# Copy the template and customize it
cp config/claude-desktop-config-template.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Option B: Manual configuration**

1. **Open the Claude Desktop config file in your editor:**
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Or use VS Code
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration (update paths for your system):**
   ```json
   {
     "mcpServers": {
       "solidworks-mcp-server": {
         "command": "/ABSOLUTE/PATH/TO/YOUR/solidworks-mcp-server/.venv/bin/python3",
         "args": ["/ABSOLUTE/PATH/TO/YOUR/solidworks-mcp-server/src/main.py"],
         "env": {
           "ANTHROPIC_API_KEY": "your-anthropic-api-key-here",
           "SOLIDWORKS_API_KEY": "your-solidworks-api-key-here",
           "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS",
           "SOLIDWORKS_VERSION": "2025",
           "CLAUDE_MODEL": "claude-3-haiku-20240307",
           "CLAUDE_MAX_TOKENS": "1000",
           "DEFAULT_EXPORT_FORMAT": "STEP",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

### Step 3: Customize Your Configuration

**Required Variables:**
- `ANTHROPIC_API_KEY`: Your real Anthropic API key
- `SOLIDWORKS_INSTALL_PATH`: Path to your SolidWorks installation

**Platform-Specific Examples:**

#### Windows Configuration:
```json
{
  "mcpServers": {
    "solidworks-mcp-server": {
      "command": "C:\\Users\\YourUsername\\solidworks-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourUsername\\solidworks-mcp-server\\src\\main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-api03-...",
        "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS",
        "SOLIDWORKS_VERSION": "2025",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### macOS Configuration:
```json
{
  "mcpServers": {
    "solidworks-mcp-server": {
      "command": "/Users/yourusername/solidworks-mcp-server/.venv/bin/python3",
      "args": ["/Users/yourusername/solidworks-mcp-server/src/main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-api03-...",
        "SOLIDWORKS_INSTALL_PATH": "/Applications/SOLIDWORKS 2025/SOLIDWORKS.app",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Step 4: Restart Claude Desktop

1. **Quit Claude Desktop completely**
2. **Restart the application**
3. **Look for the SolidWorks MCP server in the available tools**

## 🎯 Using the SolidWorks MCP Server in Claude Desktop

Once configured, you can use these commands in Claude Desktop:

### 🔄 **File Conversion**
```
Can you convert my SolidWorks part file 'bracket.sldprt' to STEP format?

Convert all parts in the 'C:\Projects\Parts' folder to STL format for 3D printing.
```

### 🔍 **File Analysis**
```
Analyze this assembly file and tell me about its design complexity and manufacturing considerations.

What are the mass properties of this part file?
```

### 🤖 **AI-Powered Insights**
```
What's the best export format for 3D printing this part?

Help me troubleshoot this conversion error: "Failed to export to IGES format"

Analyze the design intent of this CAD file and suggest improvements.
```

### 📊 **System Information**
```
Check my SolidWorks installation status.

What file formats does my SolidWorks installation support?

Show me recent conversion statistics.
```

## ⚙️ Configuration Options

### Environment Variables You Can Customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `SOLIDWORKS_VERSION` | SolidWorks version | `2025` |
| `SOLIDWORKS_VISIBLE` | Show SolidWorks UI | `false` |
| `CLAUDE_MODEL` | Claude model to use | `claude-3-haiku-20240307` |
| `CLAUDE_MAX_TOKENS` | Max response length | `1000` |
| `DEFAULT_EXPORT_FORMAT` | Default export format | `STEP` |
| `SOLIDWORKS_TIMEOUT` | API timeout (seconds) | `30` |
| `MAX_CONCURRENT_OPERATIONS` | Concurrent operations | `5` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `DEBUG_MODE` | Enable debug logging | `false` |

### Claude Model Options:
- **`claude-3-haiku-20240307`** - Fast and cost-effective (recommended)
- **`claude-3-sonnet-20240229`** - Balanced capability and speed
- **`claude-3-opus-20240229`** - Most capable for complex tasks

### SolidWorks Export Formats:
- **STEP** - Industry standard for CAD interchange
- **IGES** - Legacy CAD format
- **STL** - 3D printing and mesh applications
- **PDF** - Documentation and sharing
- **DWG/DXF** - 2D drawings and AutoCAD compatibility

## 🔍 Troubleshooting

### "spawn python ENOENT" Error

This is the most common error when starting the server. It means Claude Desktop can't find the Python executable.

**Solution:**
1. **Use absolute path to Python in virtual environment:**
   ```json
   "command": "/ABSOLUTE/PATH/TO/YOUR/solidworks-mcp-server/.venv/bin/python3"
   ```

2. **Find your Python path:**
   ```bash
   cd /path/to/solidworks-mcp-server
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   which python3  # or where python on Windows
   ```

3. **Test the path works:**
   ```bash
   "/path/to/.venv/bin/python3" --version
   ```

### Server Not Appearing in Claude Desktop

1. **Check config file syntax:**
   ```bash
   # Validate JSON syntax
   python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Verify file paths are absolute:**
   ```bash
   # Check if main.py exists
   ls -la /path/to/solidworks-mcp-server/src/main.py
   
   # Check if virtual environment exists
   ls -la /path/to/solidworks-mcp-server/.venv/bin/python3
   ```

3. **Test the server manually:**
   ```bash
   cd /path/to/solidworks-mcp-server
   source .venv/bin/activate
   python src/main.py --debug
   ```

### SolidWorks Connection Issues

1. **Verify SolidWorks installation path:**
   ```bash
   # Windows
   dir "C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS"
   
   # Check if SolidWorks is running
   tasklist | findstr SLDWORKS
   ```

2. **Test SolidWorks API access:**
   - Ensure SolidWorks is installed and licensed
   - Check if SolidWorks API is accessible
   - Verify user permissions for SolidWorks

### Environment Variable Issues

1. **Test environment variables:**
   ```bash
   # Test API key (should not be empty)
   echo $ANTHROPIC_API_KEY
   
   # Test SolidWorks path
   ls -la "$SOLIDWORKS_INSTALL_PATH"
   ```

2. **Use absolute paths everywhere** - relative paths won't work in Claude Desktop

### Permission Issues

1. **Make sure Python is accessible:**
   ```bash
   which python3  # Should show path to Python executable
   ```

2. **Check file permissions:**
   ```bash
   chmod +x /path/to/solidworks-mcp-server/src/main.py
   ```

## 📝 Example Complete Config

If you have multiple MCP servers, your config might look like:

```json
{
  "mcpServers": {
    "solidworks-mcp-server": {
      "command": "/path/to/solidworks-mcp-server/.venv/bin/python3",
      "args": ["/path/to/solidworks-mcp-server/src/main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key",
        "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS"
      }
    },
    "other-mcp-server": {
      "command": "node",
      "args": ["/path/to/other-server/index.js"]
    }
  }
}
```

## 🎉 Success!

Once configured correctly, you should see:
- SolidWorks MCP server listed in Claude Desktop's available tools
- Ability to ask Claude to help with CAD file operations
- Access to all SolidWorks tools, resources, and prompts

**Example conversation starter:**
> "Hi Claude! Can you help me with my SolidWorks files? Please check my SolidWorks installation status and show me what file formats are supported."

## 🚀 Advanced Usage Examples

### Batch Operations:
```
Convert all SLDPRT files in my project folder to STEP format for sharing with suppliers.
```

### Design Analysis:
```
Analyze this assembly for manufacturability and suggest design improvements for injection molding.
```

### Format Optimization:
```
I need to share this part with a client who uses Fusion 360. What's the best export format and settings?
```

### Troubleshooting:
```
I'm getting a "COM interface error" when trying to convert files. Can you help me troubleshoot this?
```

---

**Need help?** Check the main `DEPLOYMENT_GUIDE.md` for additional troubleshooting and usage examples.