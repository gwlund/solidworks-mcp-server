#!/usr/bin/env python3
"""
Direct SolidWorks Conversion Tool

This script demonstrates how to use the SolidWorks conversion tool directly
without an LLM, using the output directory from .env file, with input and 
output in the same location, and detailed debug messages if conversion fails.

Usage:
    python direct_conversion_tool.py <input_file_path>
    
Example:
    python direct_conversion_tool.py "C:\\path\\to\\your\\file.SLDPRT"
"""

import asyncio
import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
from tools.solidworks_tools import SolidWorksTools
from config import ConfigValidator

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('conversion_debug.log')
    ]
)

logger = logging.getLogger(__name__)

class DirectConversionTool:
    """Direct SolidWorks conversion tool without LLM."""
    
    def __init__(self):
        """Initialize the conversion tool with configuration."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.solidworks_tools = None
        self.output_directory = None
        
    def load_configuration(self) -> bool:
        """Load configuration from .env file and validate."""
        try:
            self.logger.info("Loading configuration from .env file...")
            
            # Load environment variables
            load_dotenv()
            
            # Use current directory as output directory (same location as input)
            self.output_directory = os.getcwd()
            self.logger.info(f"✅ Using current directory as output: {self.output_directory}")
            
            # Validate configuration
            config_validator = ConfigValidator()
            try:
                config_validator.validate_environment()
                self.logger.info("✅ Configuration validation successful")
            except ValueError as e:
                self.logger.error(f"❌ Configuration validation failed: {e}")
                return False
                
            self.logger.info("✅ Configuration loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error loading configuration: {e}")
            return False
    
    def initialize_solidworks_tools(self) -> bool:
        """Initialize SolidWorks tools."""
        try:
            self.logger.info("Initializing SolidWorks tools...")
            self.solidworks_tools = SolidWorksTools()
            self.logger.info("✅ SolidWorks tools initialized")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing SolidWorks tools: {e}")
            return False
    
    def validate_input_file(self, input_file_path: str) -> bool:
        """Validate input file exists and is a supported format."""
        try:
            self.logger.info(f"Validating input file: {input_file_path}")
            
            if not os.path.exists(input_file_path):
                self.logger.error(f"❌ Input file does not exist: {input_file_path}")
                return False
                
            # Check file extension
            file_ext = Path(input_file_path).suffix.upper()
            supported_formats = ['.SLDPRT', '.SLDASM', '.SLDDRW']
            
            if file_ext not in supported_formats:
                self.logger.error(f"❌ Unsupported file format: {file_ext}")
                self.logger.info(f"💡 Supported formats: {supported_formats}")
                return False
                
            file_size = os.path.getsize(input_file_path)
            self.logger.info(f"✅ Input file valid: {input_file_path} ({file_size} bytes)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error validating input file: {e}")
            return False
    
    def prepare_output_path(self, input_file_path: str) -> Optional[str]:
        """Prepare output file path in the same location as input."""
        try:
            self.logger.info("Preparing output file path...")
            
            # Get input file directory and name
            input_path = Path(input_file_path)
            input_dir = input_path.parent
            input_name = input_path.stem
            
            # Create output path in same location with .step extension
            output_file_path = input_dir / f"{input_name}.step"
            
            self.logger.info(f"✅ Output path: {output_file_path}")
            return str(output_file_path)
            
        except Exception as e:
            self.logger.error(f"❌ Error preparing output path: {e}")
            return None
    
    async def convert_file_directly(self, input_file_path: str) -> bool:
        """Convert file directly using SolidWorks tools."""
        try:
            self.logger.info("Starting direct file conversion...")
            
            # Prepare output path
            output_file_path = self.prepare_output_path(input_file_path)
            if not output_file_path:
                return False
            
            self.logger.info(f"🔄 Converting: {input_file_path} -> {output_file_path}")
            
            # Call the conversion tool directly
            result = await self.solidworks_tools.convert_file(
                input_file_path=input_file_path,
                output_file_path=output_file_path,
                export_format="STEP",
                export_options={
                    "include_hidden": True,
                    "export_sheets": True,
                    "export_sketches": False
                }
            )
            
            # Check result
            if result.get("status") == "success":
                self.logger.info("✅ Conversion completed successfully!")
                self.logger.info(f"📄 Output file: {result.get('output_file')}")
                self.logger.info(f"💬 Message: {result.get('message')}")
                
                # Verify output file exists
                if os.path.exists(output_file_path):
                    file_size = os.path.getsize(output_file_path)
                    self.logger.info(f"✅ Output file verified: {file_size} bytes")
                else:
                    self.logger.warning("⚠️ Output file not found on filesystem")
                
                return True
            else:
                self.logger.error("❌ Conversion failed!")
                self.logger.error(f"Error: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error during conversion: {e}")
            self.logger.exception("Full traceback:")
            return False
    
    async def run_conversion(self, input_file_path: str) -> bool:
        """Run the complete conversion process."""
        try:
            self.logger.info("🚀 Starting SolidWorks direct conversion process...")
            
            # Step 1: Load configuration
            if not self.load_configuration():
                return False
            
            # Step 2: Initialize SolidWorks tools
            if not self.initialize_solidworks_tools():
                return False
            
            # Step 3: Validate input file
            if not self.validate_input_file(input_file_path):
                return False
            
            # Step 4: Perform conversion
            success = await self.convert_file_directly(input_file_path)
            
            if success:
                self.logger.info("🎉 Conversion process completed successfully!")
            else:
                self.logger.error("💥 Conversion process failed!")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Fatal error in conversion process: {e}")
            self.logger.exception("Full traceback:")
            return False

def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python direct_conversion_tool.py <input_file_path>")
        print("Example: python direct_conversion_tool.py \"C:\\path\\to\\your\\file.SLDPRT\"")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    # Create and run conversion tool
    conversion_tool = DirectConversionTool()
    
    try:
        success = asyncio.run(conversion_tool.run_conversion(input_file_path))
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("⏹️ Conversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
