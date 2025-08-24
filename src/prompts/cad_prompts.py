#!/usr/bin/env python3
"""
CAD Prompts for SolidWorks MCP Server.

This module provides AI prompt templates for CAD operations
following the Single Responsibility Principle.
"""

import logging
from typing import Dict, List

import mcp.types as types

logger = logging.getLogger(__name__)


class SolidWorksPrompts:
    """
    AI prompt templates for CAD operations following SRP.
    
    This class handles all AI prompt generation for SolidWorks operations
    including analysis, format suggestions, and troubleshooting.
    """
    
    def __init__(self):
        """Initialize SolidWorks prompts."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def generate_analyze_cad_file_prompt(
        self, 
        file_path: str, 
        analysis_focus: str = None
    ) -> str:
        """Generate prompt for CAD file analysis."""
        try:
            base_prompt = f"""
You are an expert CAD engineer analyzing a SolidWorks file. Please provide a comprehensive analysis of the CAD file located at: {file_path}

Please analyze the following aspects:

1. **File Properties**:
   - File type (part, assembly, drawing)
   - Creation and modification dates
   - File size and complexity
   - SolidWorks version compatibility

2. **Design Analysis**:
   - Overall design intent and purpose
   - Key features and modeling techniques used
   - Design complexity and sophistication level
   - Potential design improvements or optimizations

3. **Manufacturing Considerations**:
   - Manufacturability assessment
   - Recommended manufacturing processes
   - Material considerations
   - Tolerance and precision requirements

4. **Performance Evaluation**:
   - Structural integrity assessment
   - Potential stress concentration areas
   - Weight optimization opportunities
   - Assembly considerations (if applicable)

5. **Quality Assessment**:
   - Model quality and best practices adherence
   - Feature tree organization
   - Parametric design effectiveness
   - Documentation completeness
"""
            
            if analysis_focus:
                focus_prompts = {
                    "design": """
Focus particularly on:
- Design methodology and approach
- Feature modeling techniques
- Parametric relationships
- Design intent capture
- Aesthetic and functional considerations
""",
                    "manufacturing": """
Focus particularly on:
- Manufacturing feasibility
- Recommended production methods
- Tooling requirements
- Material selection
- Cost optimization opportunities
- Quality control considerations
""",
                    "performance": """
Focus particularly on:
- Structural analysis potential
- Load-bearing capabilities
- Stress distribution patterns
- Fatigue considerations
- Safety factors
- Performance optimization suggestions
"""
                }
                
                if analysis_focus.lower() in focus_prompts:
                    base_prompt += focus_prompts[analysis_focus.lower()]
            
            base_prompt += """

Please provide your analysis in a structured format with clear headings and actionable insights. Include specific recommendations for improvements where applicable.
"""
            
            return base_prompt.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating analyze CAD file prompt: {e}")
            raise
    
    async def generate_suggest_export_format_prompt(
        self, 
        use_case: str, 
        file_type: str = None
    ) -> str:
        """Generate prompt for export format suggestion."""
        try:
            base_prompt = f"""
You are a CAD file format expert. A user needs to export a SolidWorks file for the following use case: {use_case}

"""
            
            if file_type:
                base_prompt += f"The source file is a SolidWorks {file_type}.\n\n"
            
            base_prompt += """
Please recommend the optimal export format(s) and provide detailed guidance including:

1. **Primary Recommendation**:
   - Recommended file format
   - Specific version or standard (if applicable)
   - Key advantages for this use case

2. **Export Settings**:
   - Recommended quality/precision settings
   - Units and coordinate system
   - Special options to enable/disable
   - File size considerations

3. **Alternative Options**:
   - Secondary format recommendations
   - Trade-offs between different formats
   - Compatibility considerations

4. **Use Case Specific Guidance**:
   - Workflow integration tips
   - Common pitfalls to avoid
   - Quality verification steps
   - Post-processing recommendations

5. **Compatibility Notes**:
   - Software compatibility
   - Version considerations
   - Platform-specific issues
   - Industry standard compliance

Please provide specific, actionable recommendations with clear reasoning for your choices.
"""
            
            return base_prompt.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating export format suggestion prompt: {e}")
            raise
    
    async def generate_troubleshoot_conversion_prompt(
        self, 
        error_message: str, 
        source_format: str = None, 
        target_format: str = None
    ) -> str:
        """Generate prompt for conversion troubleshooting."""
        try:
            base_prompt = f"""
You are a SolidWorks conversion troubleshooting expert. A user is experiencing the following error during file conversion:

**Error Message**: {error_message}

"""
            
            if source_format:
                base_prompt += f"**Source Format**: {source_format}\n"
            
            if target_format:
                base_prompt += f"**Target Format**: {target_format}\n"
            
            base_prompt += """

Please provide comprehensive troubleshooting guidance including:

1. **Error Analysis**:
   - Root cause identification
   - Common scenarios that trigger this error
   - Severity assessment (critical, moderate, minor)

2. **Immediate Solutions**:
   - Step-by-step resolution instructions
   - Quick fixes to try first
   - Settings adjustments
   - Alternative approaches

3. **Preventive Measures**:
   - Best practices to avoid this error
   - Pre-conversion checks
   - File preparation recommendations
   - Quality assurance steps

4. **Advanced Troubleshooting**:
   - Advanced diagnostic techniques
   - SolidWorks API considerations
   - System-level factors
   - Hardware/software requirements

5. **Workarounds**:
   - Alternative conversion paths
   - Intermediate format options
   - Manual intervention steps
   - Third-party tool recommendations

6. **When to Escalate**:
   - Scenarios requiring technical support
   - Data backup recommendations
   - Professional service options

Please provide clear, actionable solutions prioritized by likelihood of success and ease of implementation.
"""
            
            return base_prompt.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating troubleshooting prompt: {e}")
            raise
    
    # MCP Prompt Handler Methods
    
    async def list_prompts(self) -> List[types.Prompt]:
        """List available CAD prompts for MCP."""
        try:
            return [
                types.Prompt(
                    name="analyze_cad_file",
                    description="Analyze CAD file properties and provide insights",
                    arguments=[
                        types.PromptArgument(
                            name="file_path",
                            description="Path to the CAD file",
                            required=True
                        ),
                        types.PromptArgument(
                            name="analysis_focus",
                            description="Focus area for analysis (design, manufacturing, performance)",
                            required=False
                        )
                    ]
                ),
                types.Prompt(
                    name="suggest_export_format",
                    description="Suggest optimal export format based on use case",
                    arguments=[
                        types.PromptArgument(
                            name="use_case",
                            description="Intended use case (3D printing, simulation, sharing, etc.)",
                            required=True
                        ),
                        types.PromptArgument(
                            name="file_type",
                            description="Source file type (part, assembly, drawing)",
                            required=False
                        )
                    ]
                ),
                types.Prompt(
                    name="troubleshoot_conversion",
                    description="Help troubleshoot file conversion issues",
                    arguments=[
                        types.PromptArgument(
                            name="error_message",
                            description="Error message encountered during conversion",
                            required=True
                        ),
                        types.PromptArgument(
                            name="source_format",
                            description="Source file format",
                            required=False
                        ),
                        types.PromptArgument(
                            name="target_format", 
                            description="Target export format",
                            required=False
                        )
                    ]
                )
            ]
        except Exception as e:
            self.logger.error(f"Error listing prompts: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, str]) -> str:
        """Handle MCP prompt requests."""
        try:
            self.logger.info(f"Getting prompt {name} with arguments: {arguments}")
            
            if name == "analyze_cad_file":
                return await self.generate_analyze_cad_file_prompt(
                    file_path=arguments["file_path"],
                    analysis_focus=arguments.get("analysis_focus")
                )
            elif name == "suggest_export_format":
                return await self.generate_suggest_export_format_prompt(
                    use_case=arguments["use_case"],
                    file_type=arguments.get("file_type")
                )
            elif name == "troubleshoot_conversion":
                return await self.generate_troubleshoot_conversion_prompt(
                    error_message=arguments["error_message"],
                    source_format=arguments.get("source_format"),
                    target_format=arguments.get("target_format")
                )
            else:
                raise ValueError(f"Unknown prompt: {name}")
                
        except Exception as e:
            self.logger.error(f"Error getting prompt {name}: {e}")
            raise
