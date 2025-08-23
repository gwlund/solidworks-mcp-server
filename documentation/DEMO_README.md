# Gmail MCP Server - Email Categorization Workflow Demo

## Overview

The `demo_categorization_workflow.py` script provides a comprehensive demonstration of the email categorization workflow used in the Gmail MCP Server. This script is perfect for:

- **Executive Demonstrations**: Show how the AI email categorization works step-by-step
- **Debugging**: Understand what happens at each stage of the workflow
- **Training**: Learn how the email categorization system operates
- **Testing**: Validate the workflow with different email types and categories

## Features

### 🔴 **Live Mode (Default)**
- Uses real Gmail API and Claude AI
- Requires proper authentication setup
- Processes actual emails from your Gmail account
- Shows real AI categorization responses
- Default processes 10 emails (configurable with --max-emails)

### 🎭 **Demo Mode (Optional)**
- Uses realistic sample email data
- Simulates AI responses based on email content
- No API keys or authentication required
- Perfect for presentations and learning
- Activated with --demo flag

### 📊 **Detailed Step-by-Step Output**
The demo shows all 6 steps of the categorization workflow:

1. **Input Validation & Parameter Setup**
2. **Email Data Retrieval** (Gmail API or sample data)
3. **AI Prompt Generation** (Business logic & prompt engineering)
4. **AI Processing & Categorization** (Claude AI with temperature=0.3)
5. **Response Validation & Normalization** (Quality control)
6. **Final Results Compilation** (Structured output)

## Usage

### Live Mode (Default - processes 10 real emails)
```bash
python scripts/demo_categorization_workflow.py
```
This runs in live mode with 10 recent emails from your Gmail account.

### Demo Mode (Sample data for presentations)
```bash
python scripts/demo_categorization_workflow.py --demo
```
This runs with 10 sample emails using default categories.

### Custom Categories (Live Mode)
```bash
python scripts/demo_categorization_workflow.py --categories "High Priority,Medium Priority,Low Priority"
```

### Custom Email IDs (Live Mode)
```bash
python scripts/demo_categorization_workflow.py --email-ids "real_gmail_id_1,real_gmail_id_2"
```

### Demo Mode with Custom Settings
```bash
python scripts/demo_categorization_workflow.py --demo --max-emails 5 --categories "Work,Personal"
```

### Full Help
```bash
python scripts/demo_categorization_workflow.py --help
```

## Sample Output

The demo provides rich, colorful output showing:

- ✅ Step completion indicators
- 📧 Email details and content
- 🤖 AI prompt generation
- 🎭 AI response simulation/processing
- 🔍 Validation and error handling
- 📊 Final categorization results
- 📄 Complete JSON output

## Sample Email Data

The demo includes 5 realistic sample emails:

1. **Invoice Email** → Expected: `Receipts`
2. **Urgent Maintenance Notice** → Expected: `Urgent`
3. **Newsletter** → Expected: `Newsletters`
4. **Team Meeting** → Expected: `Work`
5. **Promotional Sale** → Expected: `Promotions`

## Key Demonstration Points

### For Your Boss
- **AI Intelligence**: Show how the system intelligently categorizes different email types
- **Consistency**: Demonstrate the temperature=0.3 setting for reliable categorization
- **Quality Control**: Show validation and error handling capabilities
- **Business Value**: Clear before/after comparison of manual vs. automated categorization

### For Debugging
- **Prompt Engineering**: See exactly what prompts are sent to Claude
- **AI Responses**: View raw AI responses before validation
- **Validation Logic**: Understand how invalid responses are handled
- **Error Handling**: See what happens when emails fail to process

### For Technical Teams
- **Temperature Configuration**: Shows environment variable usage
- **API Integration**: Demonstrates Gmail API and Claude AI integration
- **Error Recovery**: Shows graceful degradation and fallback logic
- **JSON Structure**: Complete API response format

## Requirements

### Demo Mode (Default)
- Python 3.7+
- No additional dependencies required

### Live Mode
- Python 3.7+
- Gmail API credentials configured
- Claude API key configured  
- Dependencies: `pip install -r requirements.txt`

## Pro Tips

### For Executive Demos
1. Start with: `python scripts/demo_categorization_workflow.py --demo` (sample data)
2. Point out the 6-step workflow structure  
3. Highlight the temperature=0.3 consistency feature
4. Then show live mode: `python scripts/demo_categorization_workflow.py` (real emails)
4. Show the JSON output for technical credibility

### For Technical Debugging
1. Use custom categories to test edge cases
2. Examine the prompt generation step carefully
3. Check validation logic with invalid categories
4. Review error handling with malformed email IDs

### For Performance Analysis
- Demo shows estimated timing: ~2 seconds per email
- Live mode shows actual processing time
- Validation step shows quality control effectiveness
- JSON output includes processing metadata

## Integration with Main System

This demo script uses the same `GmailTools` class as the production MCP server, ensuring that what you see in the demo is exactly how the live system behaves.

The workflow demonstrated here is the same as called by:
```python
await gmail_tools.categorize_emails(email_ids, categories)
```

---

**Perfect for board meetings, technical reviews, debugging sessions, and training new team members on the Gmail MCP Server's email categorization capabilities.**
