#!/usr/bin/env python3
"""
Configuration management for SolidWorks MCP Server.

This module handles environment variable validation and configuration
following the Single Responsibility Principle.
"""

import os
import logging
from typing import List, Optional
from dataclasses import dataclass

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Configuration data class for server settings."""
    
    # Required settings
    anthropic_api_key: str
    solidworks_api_key: str = ""
    solidworks_install_path: str = ""
    
    # SolidWorks Configuration
    solidworks_version: str = "2025"
    solidworks_visible: bool = False
    solidworks_timeout: int = 30
    solidworks_retry_attempts: int = 3
    solidworks_batch_size: int = 10
    
    # Claude AI Configuration
    claude_model: str = "claude-3-haiku-20240307"
    claude_max_tokens: int = 1000
    claude_temperature: float = 0.7
    
    # Claude Temperature Settings for Different Operations
    claude_temp_categorization: float = 0.3
    claude_temp_response_generation: float = 0.7
    claude_temp_summarization: float = 0.4
    claude_temp_action_extraction: float = 0.2
    
    # File Export Configuration
    default_export_format: str = "STEP"
    
    # Logging Configuration
    log_level: str = "INFO"
    debug_mode: bool = False
    
    # Performance Configuration
    max_concurrent_operations: int = 5
    cache_ttl_seconds: int = 300
    max_file_size_mb: int = 100
    
    # Security Configuration
    enable_audit_logging: bool = True
    max_log_file_size_mb: int = 50
    log_retention_days: int = 30


class ConfigValidator:
    """Validates and manages server configuration following SRP."""
    
    REQUIRED_VARS = [
        "ANTHROPIC_API_KEY",
    ]
    
    OPTIONAL_VARS = {
        # SolidWorks Configuration
        "SOLIDWORKS_API_KEY": "",
        "SOLIDWORKS_INSTALL_PATH": "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS",
        "SOLIDWORKS_VERSION": "2025",
        "SOLIDWORKS_VISIBLE": "false",
        "SOLIDWORKS_TIMEOUT": "30",
        "SOLIDWORKS_RETRY_ATTEMPTS": "3",
        "SOLIDWORKS_BATCH_SIZE": "10",
        
        # Claude AI Configuration
        "CLAUDE_MODEL": "claude-3-haiku-20240307",
        "CLAUDE_MAX_TOKENS": "1000",
        "CLAUDE_TEMPERATURE": "0.7",
        
        # Claude Temperature Settings
        "CLAUDE_TEMP_CATEGORIZATION": "0.3",
        "CLAUDE_TEMP_RESPONSE_GENERATION": "0.7",
        "CLAUDE_TEMP_SUMMARIZATION": "0.4",
        "CLAUDE_TEMP_ACTION_EXTRACTION": "0.2",
        
        # File Export Configuration
        "DEFAULT_EXPORT_FORMAT": "STEP",
        
        # Logging Configuration
        "LOG_LEVEL": "INFO",
        "DEBUG_MODE": "false",
        
        # Performance Configuration
        "MAX_CONCURRENT_OPERATIONS": "5",
        "CACHE_TTL_SECONDS": "300",
        "MAX_FILE_SIZE_MB": "100",
        
        # Security Configuration
        "ENABLE_AUDIT_LOGGING": "true",
        "MAX_LOG_FILE_SIZE_MB": "50",
        "LOG_RETENTION_DAYS": "30"
    }
    
    def validate_environment(self) -> None:
        """Validate required environment variables."""
        missing_vars = self._get_missing_required_vars()
        if missing_vars:
            error_msg = f"Missing required environment variables: {missing_vars}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        self._set_default_values()
        logger.info("Environment validation completed successfully")
    
    def _get_missing_required_vars(self) -> List[str]:
        """Get list of missing required environment variables."""
        return [var for var in self.REQUIRED_VARS if not os.getenv(var)]
    
    def _set_default_values(self) -> None:
        """Set default values for optional environment variables."""
        for var, default_value in self.OPTIONAL_VARS.items():
            if not os.getenv(var):
                os.environ[var] = default_value
                logger.info(f"Set default value for {var}: {default_value}")


class Config:
    """Main configuration class that provides server configuration."""
    
    def __init__(self, validator: Optional[ConfigValidator] = None):
        """Initialize configuration with optional validator dependency injection."""
        self._validator = validator or ConfigValidator()
    
    @classmethod
    def from_environment(cls) -> ServerConfig:
        """Create ServerConfig from environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        config = cls()
        config._validator.validate_environment()
        
        return ServerConfig(
            # Required settings
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            solidworks_api_key=os.getenv("SOLIDWORKS_API_KEY", ""),
            solidworks_install_path=os.getenv("SOLIDWORKS_INSTALL_PATH", "C:\\Program Files\\SOLIDWORKS Corp\\SOLIDWORKS"),
            
            # SolidWorks Configuration
            solidworks_version=os.getenv("SOLIDWORKS_VERSION", "2025"),
            solidworks_visible=os.getenv("SOLIDWORKS_VISIBLE", "false").lower() == "true",
            solidworks_timeout=int(os.getenv("SOLIDWORKS_TIMEOUT", "30")),
            solidworks_retry_attempts=int(os.getenv("SOLIDWORKS_RETRY_ATTEMPTS", "3")),
            solidworks_batch_size=int(os.getenv("SOLIDWORKS_BATCH_SIZE", "10")),
            
            # Claude AI Configuration
            claude_model=os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307"),
            claude_max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "1000")),
            claude_temperature=float(os.getenv("CLAUDE_TEMPERATURE", "0.7")),
            
            # Claude Temperature Settings
            claude_temp_categorization=float(os.getenv("CLAUDE_TEMP_CATEGORIZATION", "0.3")),
            claude_temp_response_generation=float(os.getenv("CLAUDE_TEMP_RESPONSE_GENERATION", "0.7")),
            claude_temp_summarization=float(os.getenv("CLAUDE_TEMP_SUMMARIZATION", "0.4")),
            claude_temp_action_extraction=float(os.getenv("CLAUDE_TEMP_ACTION_EXTRACTION", "0.2")),
            
            # File Export Configuration
            default_export_format=os.getenv("DEFAULT_EXPORT_FORMAT", "STEP"),
            
            # Logging Configuration
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            debug_mode=os.getenv("DEBUG_MODE", "false").lower() == "true",
            
            # Performance Configuration
            max_concurrent_operations=int(os.getenv("MAX_CONCURRENT_OPERATIONS", "5")),
            cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "300")),
            max_file_size_mb=int(os.getenv("MAX_FILE_SIZE_MB", "100")),
            
            # Security Configuration
            enable_audit_logging=os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true",
            max_log_file_size_mb=int(os.getenv("MAX_LOG_FILE_SIZE_MB", "50")),
            log_retention_days=int(os.getenv("LOG_RETENTION_DAYS", "30"))
        )
