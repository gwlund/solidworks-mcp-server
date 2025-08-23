# Claude Desktop Configuration for Gmail MCP Server

This guide shows you how to configure Claude Desktop to use your Gmail MCP server.

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

### Step 2: Add Gmail MCP Server Configuration

**Option A: Use the pre-configured file (for your specific setup)**
```bash
# Copy the ready-to-use config
cp config/claude-desktop-config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Option B: Manual configuration**

1. **Open the Claude Desktop config file in your editor:**
   ```bash
   # macOS
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Or use VS Code
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration:**
   ```json
   {
     "mcpServers": {
       "gmail-mcp-server": {
         "command": "/Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/.venv/bin/python3",
         "args": ["/Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/src/main.py"],
         "env": {
           "ANTHROPIC_API_KEY": "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",
           "GMAIL_CREDENTIALS_PATH": "/Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/credentials.json",
           "GMAIL_TOKEN_PATH": "/Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/config/token.json",
           "CLAUDE_MODEL": "claude-3-haiku-20240307",
           "CLAUDE_MAX_TOKENS": "1000",
           "CLAUDE_TEMP_CATEGORIZATION": "0.3",
           "CLAUDE_TEMP_RESPONSE_GENERATION": "0.7", 
           "CLAUDE_TEMP_SUMMARIZATION": "0.4",
           "CLAUDE_TEMP_ACTION_EXTRACTION": "0.2",
           "EMAIL_CATEGORIES": "Urgent,Work,Personal,Newsletters,Promotions,Receipts,Social,Spam",
           "DEFAULT_EMAIL_BATCH_SIZE": "10",
           "LOG_LEVEL": "INFO"
         }
       }
     }
   }
   ```

### Step 3: Restart Claude Desktop

1. **Quit Claude Desktop completely**
2. **Restart the application**
3. **Look for the Gmail MCP server in the available tools**

## 🎯 Using the Gmail MCP Server in Claude Desktop

Once configured, you can use these commands in Claude Desktop:

### 📧 **List Emails**
```
Can you show me my recent unread emails?
```

### 🏷️ **Categorize Emails**
```
Please categorize my last 10 emails into appropriate categories.
```

### ✍️ **Generate Responses**
```
Help me write a professional response to the email from [sender] about [topic].
```

### 📊 **Get Summaries**
```
Give me a summary of today's emails with action items.
```

### 📈 **View Analytics**
```
Show me my email statistics and trends.
```

## ⚙️ Configuration Options

### Environment Variables You Can Customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_MODEL` | Claude model to use | `claude-3-haiku-20240307` |
| `CLAUDE_MAX_TOKENS` | Max response length | `1000` |
| `CLAUDE_TEMPERATURE` | Response creativity (0.0-1.0) | `0.7` |
| `EMAIL_CATEGORIES` | Comma-separated categories | `Urgent,Work,Personal,...` |
| `DEFAULT_EMAIL_BATCH_SIZE` | Default emails to fetch | `10` |
| `MAX_EMAIL_BATCH_SIZE` | Maximum emails per request | `50` |
| `DEFAULT_RESPONSE_TONE` | Default response style | `professional` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `DEBUG_MODE` | Enable debug logging | `false` |

### Model Options:
- **`claude-3-haiku-20240307`** - Fast and cost-effective (recommended)
- **`claude-3-sonnet-20240229`** - Balanced capability and speed
- **`claude-3-opus-20240229`** - Most capable for complex tasks

## 🔍 Troubleshooting

### "spawn python ENOENT" Error

This is the most common error when starting the server. It means Claude Desktop can't find the Python executable.

**Solution:**
1. **Use absolute path to Python in virtual environment:**
   ```json
   "command": "/ABSOLUTE/PATH/TO/YOUR/email-mcp-server/.venv/bin/python3"
   ```

2. **Find your Python path:**
   ```bash
   cd /path/to/email-mcp-server
   source .venv/bin/activate
   which python3
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
   ls -la /Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/src/main.py
   
   # Check if credentials exist
   ls -la /Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/credentials.json
   ```

3. **Test the server manually:**
   ```bash
   cd /Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server
   source .venv/bin/activate
   python src/main.py
   ```

### Permission Issues

1. **Make sure Python is accessible:**
   ```bash
   which python
   # Should show path to Python executable
   ```

2. **Check file permissions:**
   ```bash
   chmod +x /Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/src/main.py
   ```

### Environment Variable Issues

1. **Test environment variables:**
   ```bash
   # Test API key
   echo $ANTHROPIC_API_KEY
   
   # Test credentials path
   ls -la $GMAIL_CREDENTIALS_PATH
   ```

2. **Use absolute paths everywhere** - relative paths won't work in Claude Desktop

## 📝 Example Complete Config

If you have multiple MCP servers, your config might look like:

```json
{
  "mcpServers": {
    "gmail-mcp-server": {
      "command": "python",
      "args": ["/Users/gil-lund/Library/CloudStorage/OneDrive-SharedLibraries-Onedrive/MLP/Repos/email-mcp-server/src/main.py"],
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key",
        "GMAIL_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/other-server/index.js"]
    }
  }
}
```

## 🎉 Success!

Once configured correctly, you should see:
- Gmail MCP server listed in Claude Desktop's available tools
- Ability to ask Claude to help with email management
- Access to all Gmail tools, resources, and prompts

**Example conversation starter:**
> "Hi Claude! Can you help me manage my emails? Please show me my unread messages and categorize them for me."

---

**Need help?** Check the main README.md for additional troubleshooting and usage examples.
