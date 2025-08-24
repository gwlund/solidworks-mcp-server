# Claude Desktop Setup for SolidWorks MCP Server

This guide explains how to configure Claude Desktop to work with the SolidWorks MCP Server.

## 📋 Prerequisites

1. **Claude Desktop installed** on your computer
2. **SolidWorks MCP Server deployed** and tested (see `DEPLOYMENT_GUIDE.md`)
3. **Valid Anthropic API key** (get from https://console.anthropic.com/)

## 🔧 Configuration Steps

### Step 1: Locate Claude Desktop Config File

The Claude Desktop configuration file is located at:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Update Configuration

1. **Copy the template configuration:**
   ```bash
   # From your solidworks-mcp-server directory
   cp config/claude-desktop-config-template.json ~/claude_desktop_config.json
   ```

2. **Edit the configuration file** and update the following paths:

   ```json
   {
     "mcpServers": {
       "solidworks-mcp-server": {
         "command": "/ABSOLUTE/PATH/TO/YOUR/solidworks-mcp-server/.venv/bin/python3",
         "args": ["/ABSOLUTE/PATH/TO/YOUR/solidworks-mcp-server/src/main.py"],
         "env": {
           "ANTHROPIC_API_KEY": "your-real-anthropic-api-key-here",
           "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS"
         }
       }
     }
   }
   ```

### Step 3: Customize Environment Variables

Update these key environment variables in the config:

#### **Required Variables:**
- `ANTHROPIC_API_KEY`: Your real Anthropic API key
- `SOLIDWORKS_INSTALL_PATH`: Path to your SolidWorks installation

#### **Optional Variables (customize as needed):**
- `SOLIDWORKS_VERSION`: Your SolidWorks version (default: "2025")
- `DEFAULT_EXPORT_FORMAT`: Default export format (default: "STEP")
- `LOG_LEVEL`: Logging level ("INFO", "DEBUG", "WARNING", "ERROR")
- `DEBUG_MODE`: Enable debug mode ("true" or "false")

### Step 4: Platform-Specific Path Examples

#### **Windows Example:**
```json
{
  "mcpServers": {
    "solidworks-mcp-server": {
      "command": "C:\\Users\\YourUsername\\solidworks-mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\YourUsername\\solidworks-mcp-server\\src\\main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-api03-...",
        "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### **macOS Example:**
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

### Step 5: Restart Claude Desktop

After updating the configuration:
1. **Close Claude Desktop completely**
2. **Restart Claude Desktop**
3. **Check for the SolidWorks MCP Server** in the available tools

## 🛠️ Available Tools in Claude Desktop

Once configured, you'll have access to these SolidWorks tools in Claude Desktop:

### **File Operations:**
- **convert_file**: Convert SolidWorks files to various formats (STEP, IGES, STL, PDF, etc.)
- **analyze_file**: Analyze SolidWorks files and extract properties, features, metadata
- **batch_convert**: Convert multiple SolidWorks files in batch operations

### **System Operations:**
- **validate_solidworks_installation**: Check SolidWorks installation and API availability
- **get_supported_formats**: Get list of supported import/export formats

### **AI-Powered Features:**
- **CAD Analysis Prompts**: Get AI insights about CAD file design and manufacturing
- **Export Format Suggestions**: AI recommendations for optimal export formats
- **Troubleshooting Help**: AI assistance for conversion and CAD issues

### **Data Resources:**
- **System Status**: Real-time SolidWorks installation status
- **Format Support**: Comprehensive format compatibility information
- **Export Templates**: Predefined export configurations
- **Usage Statistics**: Analytics about recent operations

## 💬 Example Usage in Claude Desktop

Once configured, you can use the SolidWorks MCP server in Claude Desktop like this:

```
"Can you convert my SolidWorks part file 'bracket.sldprt' to STEP format?"

"Analyze this assembly file and tell me about its design complexity and manufacturing considerations."

"What's the best export format for 3D printing this part?"

"I'm getting an error when converting to STL format. Can you help troubleshoot?"
```

## 🔍 Troubleshooting

### Common Issues:

1. **"MCP server not found"**
   - Check that paths in config are absolute and correct
   - Ensure virtual environment exists and Python is accessible
   - Verify the config file is in the correct location

2. **"Permission denied"**
   - Make sure Python executable has proper permissions
   - On macOS/Linux: `chmod +x .venv/bin/python3`

3. **"Module not found"**
   - Ensure dependencies are installed: `pip install -r requirements.txt`
   - Activate virtual environment before testing

4. **"SolidWorks API connection failed"**
   - Verify `SOLIDWORKS_INSTALL_PATH` is correct
   - Ensure SolidWorks is installed and accessible
   - Check SolidWorks API permissions

### Debug Mode:

Enable debug mode for troubleshooting:
```json
"env": {
  "DEBUG_MODE": "true",
  "LOG_LEVEL": "DEBUG"
}
```

### Test Configuration:

Before using with Claude Desktop, test the server directly:
```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Test server startup
python src/main.py --debug
```

## 📊 Performance Optimization

For optimal performance in Claude Desktop:

```json
"env": {
  "CLAUDE_MODEL": "claude-3-haiku-20240307",
  "MAX_CONCURRENT_OPERATIONS": "3",
  "CACHE_TTL_SECONDS": "600",
  "SOLIDWORKS_TIMEOUT": "60"
}
```

## 🔐 Security Best Practices

1. **Never commit** the actual `claude_desktop_config.json` with real API keys
2. **Use environment variables** or secure credential storage when possible
3. **Limit file access** by setting appropriate `MAX_FILE_SIZE_MB`
4. **Enable audit logging** with `ENABLE_AUDIT_LOGGING": "true"`

## 📈 Monitoring

Monitor the MCP server through:
- **Log files**: Check `solidworks_mcp.log` in the project directory
- **Claude Desktop logs**: Check Claude Desktop's internal logs
- **System resources**: Monitor CPU/memory usage during operations

---

## ✅ Configuration Checklist

- [ ] Claude Desktop installed
- [ ] SolidWorks MCP Server deployed and tested
- [ ] Configuration file created with correct paths
- [ ] Real Anthropic API key configured
- [ ] SolidWorks installation path verified
- [ ] Claude Desktop restarted
- [ ] MCP server appears in Claude Desktop tools
- [ ] Test conversion or analysis operation

**🎉 You're ready to use SolidWorks with Claude Desktop!**

## 🚀 Next Steps

1. **Test basic operations** like file conversion
2. **Explore AI-powered features** like design analysis
3. **Customize configuration** for your specific workflow
4. **Set up batch operations** for multiple files
5. **Integrate with your CAD workflow**

For more detailed information, see:
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions
- `.env.example` - All available configuration options
- `SETUP.md` - Quick start guide
