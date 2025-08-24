#!/usr/bin/env python3
"""
SolidWorks MCP Server - Main Entry Point

A Model Context Protocol server that provides SolidWorks 2025 automation capabilities
including file conversion, analysis, and CAD operations using the SolidWorks API.

This main.py file follows SOLID principles and only contains:
1. Command line argument parsing
2. Environment variable validation
3. Class initialization and dependency injection
4. MCP server startup
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Any, Dict

# Add src directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from server import MCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("solidworks_mcp.log")
    ]
)
logger = logging.getLogger("solidworks-mcp-server")


def parse_arguments() -> Dict[str, Any]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="SolidWorks MCP Server")
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug mode"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level"
    )
    parser.add_argument(
        "--log-file",
        default="solidworks_mcp.log",
        help="Log file path"
    )
    return vars(parser.parse_args())


def configure_logging(log_level: str, log_file: str, debug: bool) -> None:
    """Configure logging based on command line arguments."""
    level = getattr(logging, log_level.upper())
    if debug:
        level = logging.DEBUG
    
    # Update logging configuration
    logging.getLogger().setLevel(level)
    
    # Update file handler
    for handler in logging.getLogger().handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logging.getLogger().removeHandler(handler)
    
    logging.getLogger().addHandler(logging.FileHandler(log_file))
    logger.info(f"Logging configured: level={log_level}, file={log_file}, debug={debug}")


async def main() -> None:
    """
    Initialize and start the MCP server.
    
    This function follows SOLID principles by:
    1. Parsing command line arguments
    2. Validating environment configuration
    3. Initializing server with dependency injection
    4. Starting the server
    """
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Configure logging based on arguments
        configure_logging(
            args["log_level"], 
            args["log_file"], 
            args["debug"]
        )
        
        logger.info("Starting SolidWorks MCP Server initialization...")
        
        # Load and validate configuration from environment
        config = Config.from_environment()
        logger.info("Configuration loaded and validated successfully")
        
        # Initialize and start the MCP server with dependency injection
        server = MCPServer(config=config)
        logger.info("MCP Server initialized successfully")
        
        # Start the server
        await server.start()
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server startup error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
