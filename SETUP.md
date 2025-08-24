# SolidWorks MCP Server Setup

## Prerequisites

### Install Python 3.8+

**Windows (SolidWorks computers):**
1. Download Python from https://www.python.org/downloads/windows/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify: `python --version` in Command Prompt

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3.11 python3.11-venv python3-pip
```

## Quick Start

1. **Get the project**
   ```bash
   # Option A: Clone repository
   git clone <repository-url>
   cd solidworks-mcp-server
   
   # Option B: Download and extract ZIP file
   # Then navigate to the extracted folder
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual values
   # Required: ANTHROPIC_API_KEY
   # Optional: Customize other settings as needed
   ```

4. **Run the server**
   ```bash
   # Make sure virtual environment is activated
   python src/main.py
   
   # Or with debug mode
   python src/main.py --debug
   ```

## Troubleshooting

### Python Issues
- **"python not found"**: Ensure Python is in PATH, try `py` instead of `python` on Windows
- **Virtual environment fails**: Try `py -m venv .venv` on Windows
- **Permission errors**: Run Command Prompt as Administrator on Windows

### Dependencies Issues
- **"No module named 'mcp'"**: Activate virtual environment first, then `pip install -r requirements.txt`
- **pip fails**: Try `python -m pip install -r requirements.txt`

For detailed troubleshooting, see `DEPLOYMENT_GUIDE.md`.

## Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

### Required Variables
- `ANTHROPIC_API_KEY`: Your Anthropic Claude API key

### Optional Variables
- `SOLIDWORKS_API_KEY`: SolidWorks API key (if required)
- `SOLIDWORKS_INSTALL_PATH`: Path to SolidWorks installation
- `CLAUDE_MODEL`: Claude model to use (default: claude-3-haiku-20240307)
- And many more... see `.env.example` for complete list

## Development

Follow the SOLID principles and TDD methodology as defined in `.cursorrules`.

### Running Tests
```bash
pip install -r requirements-dev.txt
pytest
```

### Code Formatting
```bash
black src/
isort src/
flake8 src/
```
