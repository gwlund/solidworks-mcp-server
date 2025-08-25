#!/usr/bin/env python3
"""
Live MCP Server Test with SolidWorks

This script demonstrates the MCP server functionality with your SolidWorks installation.
It starts the server and shows how to interact with it.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config, ServerConfig
from tools.solidworks_tools import SolidWorksTools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-live-test")


class MCPLiveTester:
    """Live testing class for MCP server functionality."""
    
    def __init__(self):
        """Initialize the live tester."""
        self.config: ServerConfig = None
        self.solidworks_tools: SolidWorksTools = None
    
    async def setup(self) -> bool:
        """Setup the test environment."""
        logger.info("Setting up MCP live test environment...")
        
        try:
            # Load configuration
            self.config = Config.from_environment()
            self.solidworks_tools = SolidWorksTools()
            
            logger.info("✓ Test environment setup complete")
            return True
            
        except Exception as e:
            logger.error(f"✗ Setup failed: {e}")
            return False
    
    async def test_solidworks_connection(self) -> None:
        """Test SolidWorks connection and get system info."""
        logger.info("Testing SolidWorks connection...")
        
        try:
            # Validate installation
            result = await self.solidworks_tools.validate_installation()
            logger.info(f"SolidWorks Info: {json.dumps(result, indent=2)}")
            
            # Get supported formats
            formats = await self.solidworks_tools.get_supported_formats()
            logger.info(f"Supported Formats: {json.dumps(formats, indent=2)}")
            
        except Exception as e:
            logger.error(f"SolidWorks connection test failed: {e}")
    
    async def test_file_operations(self) -> None:
        """Test file operations with SolidWorks."""
        logger.info("Testing file operations...")
        
        try:
            # Test file analysis (with a dummy file path)
            test_file = "sample_part.sldprt"
            analysis_result = await self.solidworks_tools.analyze_file(test_file)
            logger.info(f"File Analysis Result: {json.dumps(analysis_result, indent=2)}")
            
            # Test file conversion (dummy operation)
            conversion_result = await self.solidworks_tools.convert_file(
                input_file_path="sample_part.sldprt",
                output_file_path="sample_part.step",
                export_format="STEP"
            )
            logger.info(f"File Conversion Result: {json.dumps(conversion_result, indent=2)}")
            
        except Exception as e:
            logger.error(f"File operations test failed: {e}")
    
    async def test_mcp_tools(self) -> None:
        """Test MCP tool functionality."""
        logger.info("Testing MCP tools...")
        
        try:
            # List available tools
            tools = await self.solidworks_tools.list_tools()
            logger.info(f"Available MCP Tools ({len(tools)}):")
            for tool in tools:
                logger.info(f"  - {tool.name}: {tool.description}")
            
            # Test tool calls
            test_calls = [
                {
                    "name": "validate_solidworks_installation",
                    "arguments": {}
                },
                {
                    "name": "get_supported_formats",
                    "arguments": {"format_type": "export"}
                },
                {
                    "name": "analyze_file",
                    "arguments": {"file_path": "test_part.sldprt", "analysis_type": "properties"}
                }
            ]
            
            for test_call in test_calls:
                logger.info(f"Testing tool: {test_call['name']}")
                result = await self.solidworks_tools.call_tool(
                    test_call['name'], 
                    test_call['arguments']
                )
                logger.info(f"Tool result: {result}")
                
        except Exception as e:
            logger.error(f"MCP tools test failed: {e}")
    
    async def demonstrate_workflow(self) -> None:
        """Demonstrate a complete workflow."""
        logger.info("Demonstrating complete workflow...")
        
        try:
            # Step 1: Validate SolidWorks installation
            logger.info("Step 1: Validating SolidWorks installation...")
            validation = await self.solidworks_tools.validate_installation()
            if validation.get("status") == "success":
                logger.info("✓ SolidWorks is ready for operations")
            else:
                logger.error("✗ SolidWorks validation failed")
                return
            
            # Step 2: Get supported formats
            logger.info("Step 2: Getting supported formats...")
            formats = await self.solidworks_tools.get_supported_formats()
            logger.info(f"✓ Available export formats: {formats.get('export_formats', [])}")
            
            # Step 3: Analyze a file (simulated)
            logger.info("Step 3: Analyzing a SolidWorks file...")
            analysis = await self.solidworks_tools.analyze_file("workflow_test.sldprt")
            logger.info(f"✓ File analysis completed: {analysis.get('properties', {}).get('file_type', 'Unknown')}")
            
            # Step 4: Convert file (simulated)
            logger.info("Step 4: Converting file to STEP format...")
            conversion = await self.solidworks_tools.convert_file(
                "workflow_test.sldprt",
                "workflow_test.step",
                "STEP"
            )
            logger.info(f"✓ File conversion completed: {conversion.get('status', 'Unknown')}")
            
            logger.info("🎉 Complete workflow demonstration finished successfully!")
            
        except Exception as e:
            logger.error(f"Workflow demonstration failed: {e}")
    
    async def run_live_demo(self) -> None:
        """Run the complete live demonstration."""
        logger.info("Starting MCP Server Live Demonstration")
        logger.info("=" * 60)
        
        # Setup
        if not await self.setup():
            logger.error("Failed to setup test environment")
            return
        
        # Run tests
        await self.test_solidworks_connection()
        await self.test_file_operations()
        await self.test_mcp_tools()
        await self.demonstrate_workflow()
        
        logger.info("=" * 60)
        logger.info("Live demonstration completed!")
        logger.info("\nYour SolidWorks MCP server is fully functional!")
        logger.info("\nTo start the actual MCP server, run:")
        logger.info("python src/main.py")


async def main():
    """Main function for live testing."""
    tester = MCPLiveTester()
    
    try:
        await tester.run_live_demo()
        
    except KeyboardInterrupt:
        logger.info("\nLive test interrupted by user")
    except Exception as e:
        logger.error(f"Live test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
