"""
SPACE CALCULATOR IMPLEMENTATION GUIDE
=====================================

This file contains 11 TODOs that need to be completed to make the space calculator functional.
Work through them in order for the best experience:

Phase 1 - Winston's Instructions (TODOs #1-#4):
- TODO #1: Add distance calculation use cases
- TODO #2: Add object coordinates description  
- TODO #3: Add gravity calculation use cases
- TODO #4: Add spacecraft mass description

Phase 2 - Distance Calculations (TODOs #5-#8):
- TODO #5: Implement 3D distance formula
- TODO #6: Convert km to AU units
- TODO #7: Calculate direction vector components
- TODO #8: Fix return statement

Phase 3 - Gravity Calculations (TODOs #9-#11):
- TODO #9: Set gravitational constant
- TODO #10: Implement Newton's law of gravitation
- TODO #11: Add missing result field

💡 TIP: Complete each section before moving to the next!
"""

import weave
import math
from typing import Dict, Any, Union, List
from tools.return_type import ToolResult

"""Phase 1 - Winston's Instructions"""
SPACE_CALCULATOR_TOOLS = {
    "calculate_distance": {
        "type": "function",
        "function": {
            "name": "space_calculator-calculate_distance",
            "description": """Calculates the distance between the spacecraft and a celestial object.
            Use this tool for:
            - Determining how far the spacecraft is from a planet, moon, star, or other celestial body
            - TODO #1: Add more use cases for distance calculations (e.g., "Calculating minimum safe distance from a black hole's event horizon")
            - Planning navigation routes and course corrections
            - Estimating travel time to destinations
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "current_coordinates": {
                        "type": "object",
                        "description": "The current coordinates of the spacecraft in 3D space (x,y,z)",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                            "z": {"type": "number"}
                        },
                        "required": ["x", "y", "z"]
                    },
                    "object_coordinates": {
                        "type": "object",
                        "description": "TODO #2: Add description for object coordinates parameter - describe what these coordinates represent in the context of space navigation",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                            "z": {"type": "number"}
                        },
                        "required": ["x", "y", "z"]
                    },
                    "unit": {
                        "type": "string",
                        "description": "The unit of measurement for the result (km, au, ly)",
                        "enum": ["km", "au", "ly"]
                    }
                },
                "required": ["current_coordinates", "object_coordinates", "unit"]
            }
        }
    },
    
    "calculate_gravity": {
        "type": "function",
        "function": {
            "name": "space_calculator-calculate_gravity",
            "description": """Calculates the gravitational force between the spacecraft and a celestial object.
            Use this tool for:
            - Determining gravitational influence of nearby celestial bodies
            - TODO #3: Add use case for escape velocity calculations
            - Assessing gravity-related dangers
            - Planning orbital maneuvers
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "spacecraft_mass": {
                        "type": "number",
                        "description": "TODO #4: Add description for spacecraft mass parameter - describe what this mass value represents and its role in gravitational calculations"
                    },
                    "object_mass": {
                        "type": "number",
                        "description": "The mass of the celestial object in kilograms"
                    },
                    "distance": {
                        "type": "number",
                        "description": "The distance between the spacecraft and the celestial object in meters"
                    }
                },
                "required": ["spacecraft_mass", "object_mass", "distance"]
            }
        }
    },
    
    "calculate_travel_time": {
        "type": "function",
        "function": {
            "name": "space_calculator-calculate_travel_time",
            "description": """Calculates the time required to travel from the current position to a destination.
            Use this tool for:
            - Planning mission durations
            - Estimating arrival times
            - Calculating fuel requirements based on journey time
            - Determining feasibility of reaching destinations
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "distance": {
                        "type": "number",
                        "description": "The distance to travel in kilometers"
                    },
                    "speed": {
                        "type": "number",
                        "description": "The spacecraft's speed in kilometers per second"
                    }
                },
                "required": ["distance", "speed"]
            }
        }
    }
}

"""Phase 2 - Distance Calculations"""
@weave.op(name="space_calculator-calculate_distance")
def calculate_distance(*, current_coordinates: Dict[str, float], 
                      object_coordinates: Dict[str, float], 
                      unit: str) -> ToolResult[Dict[str, Any]]:
    """Calculate the distance between the spacecraft and a celestial object."""
    try:
        # Extract coordinates
        x1, y1, z1 = current_coordinates["x"], current_coordinates["y"], current_coordinates["z"]
        x2, y2, z2 = object_coordinates["x"], object_coordinates["y"], object_coordinates["z"]
        
        # TODO #5: Calculate Euclidean distance in kilometers using the distance formula; Hint: Use math.sqrt and the 3D distance formula: sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
        distance_km = 0  # Replace this line with the actual calculation
        
        # Convert to requested unit
        if unit == "km":
            distance_value = distance_km
        elif unit == "au":  # Astronomical Unit
            # TODO #6: Convert km to AU (1 AU = 149,597,870.7 km)
            distance_value = distance_km  # Replace this with proper conversion
        elif unit == "ly":  # Light Year
            distance_value = distance_km / 9460730472580.8  # 1 ly = 9,460,730,472,580.8 km
        else:
            return ToolResult.err(f"Unsupported unit: {unit}")
        
        result = {
            "distance": round(distance_value, 4),
            "unit": unit,
            # TODO #7: Update vector field with direction components (x, y, z differences)
            "vector": {
                "x": 0,
                "y": 0,
                "z": 0
            }
        }
        
        # TODO #8: Return result using ToolResult.ok() wrapper instead of throwing error
        raise Exception("Function not properly implemented - check return statement")
    except Exception as e:
        return ToolResult.err(str(e))

"""Phase 3 - Gravity Calculations"""
@weave.op(name="space_calculator-calculate_gravity")
def calculate_gravity(*, spacecraft_mass: float, object_mass: float, distance: float) -> ToolResult[Dict[str, Any]]:
    """Calculate the gravitational force between the spacecraft and a celestial object."""
    try:
        # TODO #9: Set the gravitational constant (G) in m³/kg/s² - you can search online for this value
        G = 0  # Replace this with the actual gravitational constant
        
        # TODO #10: Calculate gravitational force using Newton's law: F = G * m1 * m2 / r²
        # Reference the input parameters of the function
        force = 0  # Replace this with the actual gravitational force calculation
        
        result = {
            "force_newtons": round(force, 4),
            # TODO #11: Add spacecraft_mass_kg field to show input spacecraft mass
            "object_mass_kg": object_mass,
            "distance_m": distance
        }
        
        return ToolResult.ok(result)
    except Exception as e:
        return ToolResult.err(str(e))

"""Travel Time Calculations"""
# No changes needed below this line
@weave.op(name="space_calculator-calculate_travel_time")
def calculate_travel_time(*, distance: float, speed: float) -> ToolResult[Dict[str, Any]]:
    """Calculate the time required to travel a distance at a given speed."""
    try:
        if speed <= 0:
            return ToolResult.err("Speed must be greater than zero")
        
        # Calculate time in seconds
        time_seconds = distance / speed
        
        # Convert to appropriate units
        time_minutes = time_seconds / 60
        time_hours = time_minutes / 60
        time_days = time_hours / 24
        time_years = time_days / 365.25
        
        result = {
            "seconds": round(time_seconds, 2),
            "minutes": round(time_minutes, 2),
            "hours": round(time_hours, 2),
            "days": round(time_days, 2),
            "years": round(time_years, 4)
        }
        
        return ToolResult.ok(result)
    except Exception as e:
        return ToolResult.err(str(e))