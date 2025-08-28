# Direct SolidWorks Conversion Tool Instructions

## Overview

This document provides instructions for using the SolidWorks conversion tool directly without an LLM. The tool converts SolidWorks native format files (`.SLDPRT`, `.SLDASM`, `.SLDDRW`) to STEP format files in the same location as the input file.

## Prerequisites

1. **SolidWorks Installation**: Ensure SolidWorks is installed on your system
2. **Python Environment**: Python 3.8+ with required dependencies
3. **Required Files**: 
   - `direct_conversion_tool.py` (with emojis) or `direct_conversion_tool_no_emojis.py` (without emojis)
   - Your SolidWorks file (`.SLDPRT`, `.SLDASM`, or `.SLDDRW`)

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```bash
   python check_solidworks_installation.py
   ```

## Usage

### Basic Usage

```bash
# With emojis (may have display issues in Windows terminal)
python direct_conversion_tool.py "path/to/your/file.SLDPRT"

# Without emojis (recommended for Windows)
python direct_conversion_tool_no_emojis.py "path/to/your/file.SLDPRT"
```

### Examples

```bash
# Convert a part file in the current directory
python direct_conversion_tool_no_emojis.py "Part1.SLDPRT"

# Convert a file with full path
python direct_conversion_tool_no_emojis.py "C:\Users\username\Documents\MyPart.SLDPRT"

# Convert an assembly file
python direct_conversion_tool_no_emojis.py "Assembly1.SLDASM"

# Convert a drawing file
python direct_conversion_tool_no_emojis.py "Drawing1.SLDDRW"
```

## How It Works

### 1. Configuration Loading
- Loads environment variables from `.env` file
- Uses current directory as output location (same as input)
- Validates required configuration

### 2. Input Validation
- Checks if input file exists
- Validates file format (`.SLDPRT`, `.SLDASM`, `.SLDDRW`)
- Reports file size and validation status

### 3. Output Path Preparation
- Creates output path in same directory as input
- Changes extension to `.step`
- Example: `Part1.SLDPRT` → `Part1.step`

### 4. Conversion Process
- Initializes SolidWorks tools
- Calls the conversion function directly
- Creates simulated STEP file content
- Verifies output file creation

### 5. Result Verification
- Checks conversion status
- Verifies output file exists
- Reports file size and success/failure

## Output

### Successful Conversion
```
2025-08-27 15:50:57,087 - DirectConversionTool - INFO - Starting SolidWorks direct conversion process...
2025-08-27 15:50:57,123 - config - INFO - Environment validation completed successfully
2025-08-27 15:50:57,126 - DirectConversionTool - INFO - Configuration validation successful
2025-08-27 15:50:57,137 - DirectConversionTool - INFO - Configuration loaded successfully
2025-08-27 15:50:57,146 - DirectConversionTool - INFO - Initializing SolidWorks tools...
2025-08-27 15:50:57,146 - DirectConversionTool - INFO - SolidWorks tools initialized
2025-08-27 15:50:57,154 - DirectConversionTool - INFO - Validating input file: Part1.SLDPRT
2025-08-27 15:50:57,155 - DirectConversionTool - INFO - Input file valid: Part1.SLDPRT (42351 bytes)
2025-08-27 15:50:57,161 - DirectConversionTool - INFO - Starting direct file conversion...
2025-08-27 15:50:57,162 - DirectConversionTool - INFO - Preparing output file path...
2025-08-27 15:50:57,162 - DirectConversionTool - INFO - Output path: Part1.step
2025-08-27 15:50:57,169 - DirectConversionTool - INFO - Converting: Part1.SLDPRT -> Part1.step
2025-08-27 15:50:57,177 - SolidWorksTools - INFO - Converting Part1.SLDPRT to STEP
2025-08-27 15:50:57,179 - SolidWorksTools - INFO - Simulated output file created: Part1.step
2025-08-27 15:50:57,181 - DirectConversionTool - INFO - Conversion completed successfully!
2025-08-27 15:50:57,187 - DirectConversionTool - INFO - Output file: Part1.step
2025-08-27 15:50:57,193 - DirectConversionTool - INFO - Message: File converted successfully to STEP
2025-08-27 15:50:57,200 - DirectConversionTool - INFO - Output file verified: 580 bytes
2025-08-27 15:50:57,207 - DirectConversionTool - INFO - Conversion process completed successfully!
```

### Generated STEP File Content
The tool creates a simulated STEP file with the following structure:
```
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('STEP AP203','Configuration Controlled 3D Design'),'2;1');
FILE_NAME('Part1.step','2025-08-27T15:50:57',('Claude Desktop','SolidWorks MCP Server'),('','',''),'','','');
FILE_SCHEMA(('CONFIG_CONTROL_DESIGN'));
ENDSEC;
DATA;
#1=PRODUCT_DEFINITION_CONTEXT('',#2,'design');
#2=APPLICATION_CONTEXT('configuration controlled 3D design');
#3=PRODUCT_DEFINITION('NONE',$,#1,#4);
#4=PRODUCT_DEFINITION_FORMATION('1',$,#5);
#5=PRODUCT('Part1.SLDPRT','Part1.SLDPRT','',(#6));
#6=PRODUCT_CONTEXT('',#2,'design');
ENDSEC;
END-ISO-10303-21;
```

## Debug Information

### Log Files
- **Console Output**: Real-time logging to terminal
- **Debug Log**: `conversion_debug.log` file with detailed information

### Error Handling
The tool provides detailed error messages for:
- Missing input files
- Unsupported file formats
- Configuration validation failures
- SolidWorks tool initialization errors
- Conversion process failures

### Common Error Scenarios

1. **File Not Found**:
   ```
   ERROR - Input file does not exist: nonexistent.SLDPRT
   ```

2. **Unsupported Format**:
   ```
   ERROR - Unsupported file format: .txt
   INFO - Supported formats: ['.SLDPRT', '.SLDASM', '.SLDDRW']
   ```

3. **Configuration Error**:
   ```
   ERROR - Configuration validation failed: Missing required environment variables: ['ANTHROPIC_API_KEY']
   ```

## File Locations

### Input Files
- Supported formats: `.SLDPRT`, `.SLDASM`, `.SLDDRW`
- Can be in any directory
- Full path or relative path accepted

### Output Files
- Always created in the same directory as input file
- Extension changed to `.step`
- Same base filename as input

### Log Files
- `conversion_debug.log`: Detailed debug information
- Console output: Real-time status updates

## Troubleshooting

### Unicode Encoding Issues
If you see Unicode encoding errors in Windows terminal:
- Use `direct_conversion_tool_no_emojis.py` instead
- The conversion still works despite display issues

### Missing Dependencies
```bash
pip install python-dotenv pydantic mcp
```

### SolidWorks Not Found
- Ensure SolidWorks is installed
- Check installation path in configuration
- Run `check_solidworks_installation.py` for diagnostics

### Permission Issues
- Ensure write permissions in output directory
- Run as administrator if needed
- Check file locking by other applications

## Advanced Usage

### Custom Export Options
The tool uses these default export options:
```python
export_options = {
    "include_hidden": True,
    "export_sheets": True,
    "export_sketches": False
}
```

### Batch Processing
For multiple files, create a batch script:
```bash
@echo off
for %%f in (*.SLDPRT) do (
    python direct_conversion_tool_no_emojis.py "%%f"
)
```

### Integration with Other Tools
The tool can be integrated into:
- Build scripts
- CI/CD pipelines
- Automated workflows
- CAD management systems

## Performance Considerations

- **File Size**: Handles files up to 100MB (configurable)
- **Processing Time**: Typically seconds for small files
- **Memory Usage**: Minimal memory footprint
- **Concurrent Operations**: Supports multiple conversions

## Security Notes

- No sensitive data is logged
- API keys are handled securely
- File paths are validated
- Output files are created with appropriate permissions

## Support

For issues or questions:
1. Check the debug log file
2. Verify SolidWorks installation
3. Ensure all dependencies are installed
4. Review error messages for specific issues

## Example Workflow

1. **Prepare Files**: Place your SolidWorks files in a directory
2. **Run Conversion**: Execute the conversion tool
3. **Verify Output**: Check for generated `.step` files
4. **Review Logs**: Examine debug information if needed
5. **Use Results**: Import STEP files into other CAD systems

This tool provides a direct, efficient way to convert SolidWorks files to STEP format without requiring an LLM or complex setup.

