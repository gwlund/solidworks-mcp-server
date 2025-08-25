#!/usr/bin/env python3
"""
Start SolidWorks MCP Server

This script starts the MCP server and provides instructions for testing it.
"""

import asyncio
import logging
import os
import sys
import subprocess
import time
from pathlib import Path

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config, ServerConfig
from server import MCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-server-starter")


async def start_server():
    """Start the MCP server."""
    logger.info("Starting SolidWorks MCP Server...")
    
    try:
        # Load configuration
        config = Config.from_environment()
        logger.info("✓ Configuration loaded successfully")
        
        # Initialize server
        server = MCPServer(config=config)
        logger.info("✓ MCP Server initialized successfully")
        
        # Start the server
        logger.info("🚀 Starting MCP server...")
        logger.info("The server will be available for MCP client connections.")
        logger.info("Press Ctrl+C to stop the server.")
        
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        raise


def check_prerequisites():
    """Check if all prerequisites are met."""
    logger.info("Checking prerequisites...")
    
    # Check if .env file exists
    if not Path(".env").exists():
        logger.error("✗ .env file not found. Please run check_solidworks_installation.py first.")
        return False
    
    # Check if SolidWorks is running
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq SLDWORKS.exe"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if "SLDWORKS.exe" in result.stdout:
            logger.info("✓ SolidWorks is running")
        else:
            logger.warning("⚠️  SolidWorks is not running. Starting the server anyway...")
            
    except subprocess.CalledProcessError:
        logger.warning("⚠️  Could not check if SolidWorks is running")
    
    logger.info("✓ Prerequisites check completed")
    return True


def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("SolidWorks MCP Server - Usage Instructions")
    print("=" * 60)
    print("\nThe MCP server is now running and ready to accept connections.")
    print("\nTo test the server with an MCP client:")
    print("\n1. Install an MCP client (like Claude Desktop):")
    print("   - Download from: https://claude.ai/desktop")
    print("   - Or use another MCP-compatible client")
    print("\n2. Configure the client to connect to this server:")
    print("   - Server type: stdio")
    print("   - Command: python")
    print("   - Args: ['src/main.py']")
    print("   - Working directory: [path to this project]")
    print("\n3. Available tools:")
    print("   - convert_file: Convert SolidWorks files to different formats")
    print("   - analyze_file: Analyze SolidWorks file properties and features")
    print("   - batch_convert: Convert multiple files in batch")
    print("   - validate_solidworks_installation: Check SolidWorks setup")
    print("   - get_supported_formats: List supported file formats")
    print("\n4. Example usage in Claude Desktop:")
    print("   'Convert my SolidWorks part file to STEP format'")
    print("   'Analyze the properties of my assembly file'")
    print("   'What file formats can SolidWorks export?'")
    print("\n" + "=" * 60)


async def main():
    """Main function."""
    print("SolidWorks MCP Server Starter")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        return
    
    # Print instructions
    print_usage_instructions()
    
    # Start the server
    await start_server()


if __name__ == "__main__":
    asyncio.run(main())
