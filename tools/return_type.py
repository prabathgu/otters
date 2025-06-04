from typing import TypeVar, Generic, Optional
import json
T = TypeVar('T')
class ToolResult(Generic[T]):
    """Represents the result of a tool operation."""
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def ok(cls, data: T) -> 'ToolResult[T]':
        """Create a successful result"""
        return cls(success=True, data=data)
    
    @classmethod
    def err(cls, error: str) -> 'ToolResult[T]':
        """Create a failed result"""
        if not error.startswith("Error: "):
            error = f"Error: {error}"
        return cls(success=False, error=error)
    
    def __bool__(self) -> bool:
        """Allows using Result in if statements directly"""
        return self.success
    
    def __str__(self) -> str:
        """String representation for print() and str()"""
        if self.success:
            return json.dumps({
                "status": "success",
                "data": self.data,
            })
        else:
            return json.dumps({
                "status": "error",
                "error": self.error
            })
            
    def __repr__(self) -> str:
        """String representation for direct access"""
        return self.__str__()
