#!/usr/bin/env python3
"""
SolidWorks MCP Server Integration Test Script

This script tests the MCP server with your SolidWorks installation to validate:
1. Environment configuration
2. SolidWorks API connectivity
3. MCP server functionality
4. Tool operations

Run this script to test your setup before using the MCP server.
"""

import asyncio
import os
import sys
import logging
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
logger = logging.getLogger("solidworks-test")


class SolidWorksIntegrationTester:
    """Test class for SolidWorks MCP server integration."""
    
    def __init__(self):
        """Initialize the tester."""
        self.config: ServerConfig = None
        self.solidworks_tools: SolidWorksTools = None
    
    async def test_environment_setup(self) -> bool:
        """Test environment configuration."""
        logger.info("Testing environment configuration...")
        
        try:
            # Test if .env file exists
            env_file = Path(".env")
            if not env_file.exists():
                logger.warning("No .env file found. Creating one with default values...")
                self._create_default_env_file()
            
            # Load configuration
            self.config = Config.from_environment()
            logger.info("✓ Environment configuration loaded successfully")
            
            # Validate required settings
            if not self.config.anthropic_api_key:
                logger.error("✗ ANTHROPIC_API_KEY is required but not set")
                return False
            
            logger.info("✓ Required environment variables validated")
            return True
            
        except Exception as e:
            logger.error(f"✗ Environment setup failed: {e}")
            return False
    
    def _create_default_env_file(self) -> None:
        """Create a default .env file for testing."""
        env_content = """# SolidWorks MCP Server Environment Configuration
# Update these values with your actual configuration

# REQUIRED: Anthropic Claude API Key
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# SolidWorks Configuration
SOLIDWORKS_API_KEY=your_solidworks_api_key_here
SOLIDWORKS_INSTALL_PATH=C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS
SOLIDWORKS_VERSION=2025
SOLIDWORKS_VISIBLE=false
SOLIDWORKS_TIMEOUT=30
SOLIDWORKS_RETRY_ATTEMPTS=3
SOLIDWORKS_BATCH_SIZE=10

# Claude AI Configuration
CLAUDE_MODEL=claude-3-haiku-20240307
CLAUDE_MAX_TOKENS=1000
CLAUDE_TEMPERATURE=0.7

# Claude Temperature Settings
CLAUDE_TEMP_CATEGORIZATION=0.3
CLAUDE_TEMP_RESPONSE_GENERATION=0.7
CLAUDE_TEMP_SUMMARIZATION=0.4
CLAUDE_TEMP_ACTION_EXTRACTION=0.2

# File Export Configuration
DEFAULT_EXPORT_FORMAT=STEP

# Logging Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false

# Performance Configuration
MAX_CONCURRENT_OPERATIONS=5
CACHE_TTL_SECONDS=300
MAX_FILE_SIZE_MB=100

# Security Configuration
ENABLE_AUDIT_LOGGING=true
MAX_LOG_FILE_SIZE_MB=50
LOG_RETENTION_DAYS=30
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        logger.info("Created .env file with default values. Please update with your actual configuration.")
    
    async def test_solidworks_installation(self) -> bool:
        """Test SolidWorks installation and API connectivity."""
        logger.info("Testing SolidWorks installation...")
        
        try:
            # Initialize SolidWorks tools
            self.solidworks_tools = SolidWorksTools()
            
            # Test installation validation
            result = await self.solidworks_tools.validate_installation()
            
            if result.get("status") == "success":
                logger.info("✓ SolidWorks installation validated")
                logger.info(f"  Version: {result.get('version', 'Unknown')}")
                logger.info(f"  API Available: {result.get('api_available', False)}")
                logger.info(f"  License Valid: {result.get('license_valid', False)}")
                return True
            else:
                logger.error("✗ SolidWorks installation validation failed")
                return False
                
        except Exception as e:
            logger.error(f"✗ SolidWorks installation test failed: {e}")
            return False
    
    async def test_supported_formats(self) -> bool:
        """Test getting supported file formats."""
        logger.info("Testing supported file formats...")
        
        try:
            result = await self.solidworks_tools.get_supported_formats()
            
            if result.get("status") == "success":
                logger.info("✓ Supported formats retrieved successfully")
                logger.info(f"  Import formats: {result.get('import_formats', [])}")
                logger.info(f"  Export formats: {result.get('export_formats', [])}")
                return True
            else:
                logger.error("✗ Failed to get supported formats")
                return False
                
        except Exception as e:
            logger.error(f"✗ Supported formats test failed: {e}")
            return False
    
    async def test_mcp_tools(self) -> bool:
        """Test MCP tool listing and functionality."""
        logger.info("Testing MCP tools...")
        
        try:
            # Test tool listing
            tools = await self.solidworks_tools.list_tools()
            
            if tools:
                logger.info("✓ MCP tools listed successfully")
                for tool in tools:
                    logger.info(f"  - {tool.name}: {tool.description}")
                return True
            else:
                logger.error("✗ No MCP tools found")
                return False
                
        except Exception as e:
            logger.error(f"✗ MCP tools test failed: {e}")
            return False
    
    async def test_file_analysis(self) -> bool:
        """Test file analysis functionality."""
        logger.info("Testing file analysis...")
        
        try:
            # Create a test file path (this would be a real SolidWorks file in practice)
            test_file_path = "test_part.sldprt"
            
            result = await self.solidworks_tools.analyze_file(test_file_path)
            
            if result.get("status") == "success":
                logger.info("✓ File analysis test completed")
                logger.info(f"  File type: {result.get('properties', {}).get('file_type', 'Unknown')}")
                return True
            else:
                logger.error("✗ File analysis test failed")
                return False
                
        except Exception as e:
            logger.error(f"✗ File analysis test failed: {e}")
            return False
    
    async def test_server_startup(self) -> bool:
        """Test MCP server startup (without actually starting it)."""
        logger.info("Testing MCP server initialization...")
        
        try:
            from server import MCPServer
            
            # Test server initialization
            server = MCPServer(config=self.config)
            logger.info("✓ MCP server initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"✗ MCP server initialization failed: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all integration tests."""
        logger.info("Starting SolidWorks MCP Server Integration Tests")
        logger.info("=" * 50)
        
        test_results = {}
        
        # Run tests in sequence
        tests = [
            ("Environment Setup", self.test_environment_setup),
            ("SolidWorks Installation", self.test_solidworks_installation),
            ("Supported Formats", self.test_supported_formats),
            ("MCP Tools", self.test_mcp_tools),
            ("File Analysis", self.test_file_analysis),
            ("Server Initialization", self.test_server_startup),
        ]
        
        for test_name, test_func in tests:
            logger.info(f"\nRunning {test_name} test...")
            try:
                result = await test_func()
                test_results[test_name] = result
            except Exception as e:
                logger.error(f"Test {test_name} failed with exception: {e}")
                test_results[test_name] = False
        
        return test_results
    
    def print_test_summary(self, results: Dict[str, bool]) -> None:
        """Print test results summary."""
        logger.info("\n" + "=" * 50)
        logger.info("TEST RESULTS SUMMARY")
        logger.info("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✓ PASS" if result else "✗ FAIL"
            logger.info(f"{test_name}: {status}")
        
        logger.info(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            logger.info("🎉 All tests passed! Your SolidWorks MCP server is ready to use.")
        else:
            logger.warning("⚠️  Some tests failed. Please check the configuration and try again.")
            logger.info("\nNext steps:")
            logger.info("1. Update your .env file with correct API keys")
            logger.info("2. Ensure SolidWorks is properly installed")
            logger.info("3. Verify SolidWorks API access")
            logger.info("4. Run the tests again")


async def main():
    """Main test function."""
    tester = SolidWorksIntegrationTester()
    
    try:
        results = await tester.run_all_tests()
        tester.print_test_summary(results)
        
    except KeyboardInterrupt:
        logger.info("\nTests interrupted by user")
    except Exception as e:
        logger.error(f"Test execution failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
