"""
Base Tool Template for Phase 3 Multi-Agent System
All tools (RAG Retriever, BanglaBERT Validator) inherit from this
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel, Field
import sys
from pathlib import Path

# Add config to path
sys.path.append(str(Path(__file__).parent.parent / "config"))
from logging_config import setup_logger


class ToolInput(BaseModel):
    """Base input schema for all tools"""
    pass


class ToolOutput(BaseModel):
    """Base output schema for all tools"""
    success: bool = Field(description="Whether tool execution succeeded")
    data: Any = Field(description="Tool output data")
    error: str = Field(default="", description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class BaseTool(ABC):
    """
    Abstract base class for all agent tools
    Ensures consistent interface and error handling
    """
    
    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(f"Tool.{name}")
        self.logger.info(f"Initializing {name} tool")
    
    @abstractmethod
    def _execute(self, input_data: ToolInput) -> ToolOutput:
        """
        Core tool logic - must be implemented by subclasses
        
        Args:
            input_data: Validated input data
            
        Returns:
            ToolOutput with results
        """
        pass
    
    def run(self, input_data: ToolInput) -> ToolOutput:
        """
        Execute tool with error handling and logging
        
        Args:
            input_data: Tool input
            
        Returns:
            ToolOutput with results or error
        """
        try:
            self.logger.info(f"Running {self.name} tool")
            self.logger.debug(f"Input: {input_data}")
            
            # Execute core logic
            output = self._execute(input_data)
            
            self.logger.info(f"{self.name} completed successfully")
            self.logger.debug(f"Output: {output}")
            
            return output
            
        except Exception as e:
            self.logger.error(f"{self.name} failed: {str(e)}", exc_info=True)
            return ToolOutput(
                success=False,
                data=None,
                error=str(e),
                metadata={"tool": self.name}
            )
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


# Example Tool Implementation
class ExampleToolInput(ToolInput):
    """Example input schema"""
    text: str = Field(description="Input text")


class ExampleTool(BaseTool):
    """Example tool demonstrating the pattern"""
    
    def __init__(self):
        super().__init__(name="ExampleTool")
    
    def _execute(self, input_data: ExampleToolInput) -> ToolOutput:
        """Example implementation"""
        result = f"Processed: {input_data.text}"
        return ToolOutput(
            success=True,
            data=result,
            metadata={"length": len(input_data.text)}
        )


if __name__ == "__main__":
    # Test the base tool
    print("🧪 Testing Base Tool Template\n")
    
    tool = ExampleTool()
    test_input = ExampleToolInput(text="Hello, Multi-Agent System!")
    
    output = tool.run(test_input)
    
    print(f"\n✅ Tool Output:")
    print(f"  Success: {output.success}")
    print(f"  Data: {output.data}")
    print(f"  Metadata: {output.metadata}")
