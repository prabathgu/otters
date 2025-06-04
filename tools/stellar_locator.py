import weave
import math
import random
from typing import Dict, Any, List, Optional, Union
from tools.return_type import ToolResult
from .celestrial_objects import CELESTIAL_OBJECTS

STELLAR_LOCATOR_TOOLS = {
    "locate_celestial_object": {
        "type": "function",
        "function": {
            "name": "stellar_locator-locate_celestial_object",
            "description": """Locates planets, space stations, or other celestial objects in the galaxy.
            Use this tool for:
            - Finding the exact location of known celestial bodies
            - Discovering what exists at specific coordinates
            - Getting information about planets, moons, stations, or probes
            - Planning navigation routes to destinations
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "coordinates": {
                        "type": "object",
                        "description": "The coordinates to search in galactic grid format",
                        "properties": {
                            "sector": {"type": "string", "description": "Alpha-numeric sector designation (e.g., 'A7', 'C12')"},
                            "quadrant": {"type": "string", "description": "Quadrant within sector (NE, NW, SE, SW)"},
                            "x": {"type": "number", "description": "X-coordinate within quadrant (0-999)"},
                            "y": {"type": "number", "description": "Y-coordinate within quadrant (0-999)"},
                            "z": {"type": "number", "description": "Z-coordinate within quadrant (0-999)"}
                        },
                        "required": ["sector", "quadrant", "x", "y", "z"]
                    }
                },
                "required": ["coordinates"]
            }
        }
    },
    
    "search_by_name": {
        "type": "function",
        "function": {
            "name": "stellar_locator-search_by_name",
            "description": """Searches for celestial objects by name or partial name.
            Use this tool for:
            - Finding the coordinates of a known planet, station, or probe
            - Getting information about a celestial body when you only know its name
            - Discovering objects with similar names or in the same system
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Full or partial name of the celestial object to search for"
                    },
                    "object_type": {
                        "type": "string",
                        "description": "Type of object to search for (optional)",
                        "enum": ["planet", "moon", "star", "station", "probe", "anomaly", "any"]
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximum number of results to return (default: 5)"
                    }
                },
                "required": ["name"]
            }
        }
    },
    
    "scan_region": {
        "type": "function",
        "function": {
            "name": "stellar_locator-scan_region",
            "description": """Scans a region of space to identify all celestial objects within it.
            Use this tool for:
            - Mapping unknown regions of space
            - Finding all objects in a particular sector or quadrant
            - Checking for hazards or resources in an area
            - Discovering hidden or cloaked objects with deep scans
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "sector": {
                        "type": "string",
                        "description": "Alpha-numeric sector designation (e.g., 'A7', 'C12')"
                    },
                    "quadrant": {
                        "type": "string",
                        "description": "Quadrant to scan (NE, NW, SE, SW, or 'all' for entire sector)",
                        "enum": ["NE", "NW", "SE", "SW", "all"]
                    },
                    "scan_depth": {
                        "type": "string",
                        "description": "Depth of scan (deeper scans reveal more hidden objects)",
                        "enum": ["standard", "deep", "ultra"]
                    }
                },
                "required": ["sector", "quadrant", "scan_depth"]
            }
        }
    }
}

# Database of celestial objects
# In a real implementation, this would be stored in a database

@weave.op(name="stellar_locator-locate_celestial_object")
def locate_celestial_object(*, coordinates: Dict[str, Any]) -> ToolResult[Dict[str, Any]]:
    """Locate a celestial object at the given coordinates."""
    try:
        # Validate coordinates
        required_fields = ["sector", "quadrant", "x", "y", "z"]
        for field in required_fields:
            if field not in coordinates:
                return ToolResult.err(f"Missing required coordinate: {field}")
                
        # Check for valid quadrant
        if coordinates["quadrant"] not in ["NE", "NW", "SE", "SW"]:
            return ToolResult.err(f"Invalid quadrant: {coordinates['quadrant']}. Must be NE, NW, SE, or SW.")
            
        # Check for valid numerical coordinates
        for coord in ["x", "y", "z"]:
            if not isinstance(coordinates[coord], (int, float)) or coordinates[coord] < 0 or coordinates[coord] > 999:
                return ToolResult.err(f"Invalid {coord} coordinate: {coordinates[coord]}. Must be a number between 0-999.")
        
        # Look for exact matches
        exact_match = None
        for obj in CELESTIAL_OBJECTS:
            if (obj["coordinates"]["sector"] == coordinates["sector"] and
                obj["coordinates"]["quadrant"] == coordinates["quadrant"] and
                abs(obj["coordinates"]["x"] - coordinates["x"]) <= 2 and
                abs(obj["coordinates"]["y"] - coordinates["y"]) <= 2 and
                abs(obj["coordinates"]["z"] - coordinates["z"]) <= 2):
                
                # Skip hidden objects in normal searches
                if obj["hidden"]:
                    continue
                    
                exact_match = obj
                break
        
        if exact_match:
            return ToolResult.ok({
                "found": True,
                "object": {
                    "name": exact_match["name"],
                    "type": exact_match["type"],
                    "class": exact_match["class"],
                    "description": exact_match["description"],
                    "status": exact_match["status"],
                    "exact_coordinates": exact_match["coordinates"]
                }
            })
        
        # If no exact match, find nearest objects
        nearest_objects = []
        for obj in CELESTIAL_OBJECTS:
            if obj["hidden"]:
                continue
                
            if obj["coordinates"]["sector"] == coordinates["sector"]:
                # Only consider objects in the same sector
                distance = calculate_distance_3d(
                    coordinates["x"], coordinates["y"], coordinates["z"],
                    obj["coordinates"]["x"], obj["coordinates"]["y"], obj["coordinates"]["z"]
                )
                
                nearest_objects.append({
                    "name": obj["name"],
                    "type": obj["type"],
                    "distance": distance,
                    "coordinates": obj["coordinates"]
                })
        
        nearest_objects.sort(key=lambda x: x["distance"])
        nearest_objects = nearest_objects[:3]  # Only return the 3 nearest
        
        if nearest_objects:
            return ToolResult.ok({
                "found": False,
                "message": "No exact match found at these coordinates.",
                "nearest_objects": nearest_objects
            })
        
        # No objects found in sector
        return ToolResult.ok({
            "found": False,
            "message": f"No celestial objects found in sector {coordinates['sector']}.",
            "nearest_objects": []
        })
    except Exception as e:
        return ToolResult.err(f"Error locating object: {str(e)}")

@weave.op(name="stellar_locator-search_by_name")
def search_by_name(*, name: str, object_type: str = "any", max_results: int = 5) -> ToolResult[Dict[str, Any]]:
    """Search for celestial objects by name."""
    try:
        if not name:
            return ToolResult.err("Name parameter cannot be empty")
            
        name = name.lower()
        results = []
        
        for obj in CELESTIAL_OBJECTS:
            # Skip hidden objects in normal searches
            if obj["hidden"]:
                continue
                
            # Apply type filter if specified
            if object_type != "any" and obj["type"] != object_type:
                continue
                
            # For exact matches
            obj_name_lower = obj["name"].lower()
            
            # Handle exact name search case
            if name == obj_name_lower:
                results.append({
                    "name": obj["name"],
                    "type": obj["type"],
                    "class": obj["class"],
                    "coordinates": obj["coordinates"],
                    "status": obj["status"],
                    "description": obj["description"]
                })
                # If we find an exact match for an exact name search, only return that one
                if name == obj_name_lower and len(name.split()) > 1:
                    return ToolResult.ok({
                        "found": True,
                        "count": 1,
                        "results": [results[-1]]
                    })
                continue
                
            # For partial matches
            if name in obj_name_lower:
                results.append({
                    "name": obj["name"],
                    "type": obj["type"],
                    "class": obj["class"],
                    "coordinates": obj["coordinates"],
                    "status": obj["status"],
                    "description": obj["description"]
                })
        
        # Sort results by exact match first, then alphabetically
        results.sort(key=lambda x: (0 if x["name"].lower() == name else 1, x["name"]))
        
        # Limit results
        results = results[:max_results]
        
        if results:
            return ToolResult.ok({
                "found": True,
                "count": len(results),
                "results": results
            })
        else:
            return ToolResult.ok({
                "found": False,
                "message": f"No celestial objects found matching '{name}'.",
                "count": 0,
                "results": []
            })
    except Exception as e:
        return ToolResult.err(f"Error searching for object: {str(e)}")

@weave.op(name="stellar_locator-scan_region")
def scan_region(*, sector: str, quadrant: str, scan_depth: str) -> ToolResult[Dict[str, Any]]:
    """Scan a region to discover celestial objects."""
    try:
        if not sector:
            return ToolResult.err("Sector parameter cannot be empty")
            
        if quadrant not in ["NE", "NW", "SE", "SW", "all"]:
            return ToolResult.err(f"Invalid quadrant: {quadrant}. Must be NE, NW, SE, SW, or 'all'")
            
        if scan_depth not in ["standard", "deep", "ultra"]:
            return ToolResult.err(f"Invalid scan depth: {scan_depth}. Must be 'standard', 'deep', or 'ultra'")
        
        # Determine scan effectiveness based on depth
        reveal_hidden = False
        if scan_depth == "deep":
            reveal_hidden = random.random() < 0.5  # 50% chance to detect hidden objects
        elif scan_depth == "ultra":
            reveal_hidden = True  # Always detect hidden objects
        
        results = []
        for obj in CELESTIAL_OBJECTS:
            # Filter by sector
            if obj["coordinates"]["sector"] != sector:
                continue
                
            # Filter by quadrant (if not "all")
            if quadrant != "all" and obj["coordinates"]["quadrant"] != quadrant:
                continue
                
            # Filter hidden objects based on scan depth
            if obj["hidden"] and not reveal_hidden:
                continue
            
            # Add object to results
            results.append({
                "name": obj["name"],
                "type": obj["type"],
                "class": obj["class"],
                "coordinates": obj["coordinates"],
                "status": obj["status"]
            })
        
        # Add descriptive scan information
        scan_info = {
            "sector": sector,
            "quadrant": quadrant if quadrant != "all" else "Full sector scan",
            "scan_depth": scan_depth,
            "scan_power": "Standard" if scan_depth == "standard" else "Enhanced" if scan_depth == "deep" else "Maximum"
        }
        
        if results:
            unknown_count = 0
            if scan_depth != "ultra":
                # Add a hint about possible hidden objects
                hidden_in_region = sum(1 for obj in CELESTIAL_OBJECTS 
                                    if obj["hidden"] and obj["coordinates"]["sector"] == sector and
                                    (quadrant == "all" or obj["coordinates"]["quadrant"] == quadrant))
                                    
                if hidden_in_region > 0 and not reveal_hidden:
                    unknown_count = hidden_in_region
        
            return ToolResult.ok({
                "scan_info": scan_info,
                "found": True,
                "count": len(results),
                "objects": results,
                "unknown_signatures": unknown_count
            })
        else:
            return ToolResult.ok({
                "scan_info": scan_info,
                "found": False,
                "message": f"No celestial objects detected in {sector} {quadrant}.",
                "count": 0,
                "objects": []
            })
    except Exception as e:
        return ToolResult.err(f"Scan error: {str(e)}")

# Helper functions
def calculate_distance_3d(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    """Calculate the Euclidean distance between two 3D points."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)