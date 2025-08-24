#!/usr/bin/env python3
"""
MCP Server for SolidWorks integration.

This module contains the main MCP server class that follows SOLID principles,
specifically the Single Responsibility Principle and Dependency Inversion Principle.
"""

import logging
from typing import Optional

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from config import ServerConfig
from tools.solidworks_tools import SolidWorksTools
from resources.cad_resources import CADResources
from prompts.cad_prompts import SolidWorksPrompts

logger = logging.getLogger(__name__)


class MCPServer:
    """
    Main MCP Server class following Single Responsibility Principle.
    
    This class is responsible only for coordinating the MCP server lifecycle
    and registering handlers. All business logic is delegated to specialized handlers.
    """
    
    def __init__(
        self,
        config: ServerConfig,
        solidworks_tools: Optional[SolidWorksTools] = None,
        cad_resources: Optional[CADResources] = None,
        solidworks_prompts: Optional[SolidWorksPrompts] = None
    ):
        """
        Initialize MCP server with dependency injection (DIP).
        
        Args:
            config: Server configuration
            solidworks_tools: Optional SolidWorks tools (for testing/customization)
            cad_resources: Optional CAD resources (for testing/customization)
            solidworks_prompts: Optional SolidWorks prompts (for testing/customization)
        """
        self._config = config
        self._server = Server("solidworks-mcp-server")
        
        # Initialize components with dependency injection
        self._initialize_components(solidworks_tools, cad_resources, solidworks_prompts)
        
        # Register MCP handlers
        self._register_handlers()
    
    def _initialize_components(
        self,
        solidworks_tools: Optional[SolidWorksTools],
        cad_resources: Optional[CADResources],
        solidworks_prompts: Optional[SolidWorksPrompts]
    ) -> None:
        """Initialize server components with dependency injection."""
        try:
            # Initialize components with dependency injection
            self._solidworks_tools = solidworks_tools or SolidWorksTools()
            self._cad_resources = cad_resources or CADResources()
            self._solidworks_prompts = solidworks_prompts or SolidWorksPrompts()
            
            logger.info("All server components initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize server components: {e}")
            raise
    
    def _register_handlers(self) -> None:
        """Register MCP handlers with the server."""
        # Register tool handlers
        @self._server.list_tools()
        async def handle_list_tools():
            return await self._solidworks_tools.list_tools()
        
        @self._server.call_tool()
        async def handle_call_tool(name: str, arguments: dict):
            return await self._solidworks_tools.call_tool(name, arguments)
        
        # Register resource handlers
        @self._server.list_resources()
        async def handle_list_resources():
            return await self._cad_resources.list_resources()
        
        @self._server.read_resource()
        async def handle_read_resource(uri: str):
            return await self._cad_resources.read_resource(uri)
        
        # Register prompt handlers
        @self._server.list_prompts()
        async def handle_list_prompts():
            return await self._solidworks_prompts.list_prompts()
        
        @self._server.get_prompt()
        async def handle_get_prompt(name: str, arguments: dict):
            prompt_content = await self._solidworks_prompts.get_prompt(name, arguments)
            return types.GetPromptResult(
                description=f"AI prompt for {name}",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(type="text", text=prompt_content)
                    )
                ]
            )
        
        logger.info("All MCP handlers registered successfully")
    
    async def start(self) -> None:
        """Start the MCP server."""
        logger.info("Starting SolidWorks MCP Server...")
        
        # Create initialization options
        init_options = InitializationOptions(
            server_name="solidworks-mcp-server",
            server_version="1.0.0"
        )
        
        async with stdio_server() as (read_stream, write_stream):
            await self._server.run(
                read_stream,
                write_stream,
                init_options
            )
