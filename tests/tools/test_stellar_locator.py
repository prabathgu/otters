import unittest
from unittest.mock import patch, MagicMock
from tools.stellar_locator import (
    locate_celestial_object,
    search_by_name,
    scan_region,
    CELESTIAL_OBJECTS
)
from tools.return_type import ToolResult

class TestStellarLocator(unittest.TestCase):
    def test_locate_celestial_object_exact_match(self):
        # Test locating New Terra using its exact coordinates
        result = locate_celestial_object(
            coordinates={
                "sector": "A7",
                "quadrant": "NE",
                "x": 453,
                "y": 127,
                "z": 89
            }
        )
        
        self.assertTrue(result.success)
        self.assertTrue(result.data["found"])
        self.assertEqual(result.data["object"]["name"], "New Terra")
        self.assertEqual(result.data["object"]["type"], "planet")
        
    def test_locate_celestial_object_nearby(self):
        # Test finding an object that is close but not exact
        result = locate_celestial_object(
            coordinates={
                "sector": "A7",
                "quadrant": "NE",
                "x": 450,
                "y": 130,
                "z": 90
            }
        )
        
        self.assertTrue(result.success)
        self.assertFalse(result.data["found"])
        self.assertTrue(len(result.data["nearest_objects"]) > 0)
        
    def test_locate_celestial_object_invalid_coordinates(self):
        # Test with invalid coordinates
        result = locate_celestial_object(
            coordinates={
                "sector": "A7",
                "quadrant": "XYZ",  # Invalid quadrant
                "x": 453,
                "y": 127,
                "z": 89
            }
        )
        
        self.assertFalse(result.success)
        self.assertIn("Invalid quadrant", result.error)
        
    def test_search_by_name_exact(self):
        # Test searching for a celestial object by exact name
        result = search_by_name(
            name="New Terra"
        )
        
        self.assertTrue(result.success)
        self.assertTrue(result.data["found"])
        self.assertEqual(result.data["count"], 1)
        self.assertEqual(result.data["results"][0]["name"], "New Terra")
        
    def test_search_by_name_partial(self):
        # Test searching for objects with partial name match
        result = search_by_name(
            name="Terra"
        )
        
        self.assertTrue(result.success)
        self.assertTrue(result.data["found"])
        self.assertTrue(result.data["count"] >= 2)  # Should find New Terra and New Terra Alpha
        
    def test_search_by_name_with_type_filter(self):
        # Test searching with type filter
        result = search_by_name(
            name="Terra",
            object_type="moon"
        )
        
        self.assertTrue(result.success)
        self.assertTrue(result.data["found"])
        self.assertEqual(result.data["count"], 1)
        self.assertEqual(result.data["results"][0]["name"], "New Terra Alpha")
        self.assertEqual(result.data["results"][0]["type"], "moon")
        
    def test_search_by_name_no_results(self):
        # Test search with no results
        result = search_by_name(
            name="NonExistentPlanet"
        )
        
        self.assertTrue(result.success)
        self.assertFalse(result.data["found"])
        self.assertEqual(result.data["count"], 0)
        
    def test_scan_region_standard(self):
        # Test standard scan of a region
        result = scan_region(
            sector="A7",
            quadrant="NE",
            scan_depth="standard"
        )
        
        self.assertTrue(result.success)
        self.assertTrue(result.data["found"])
        # Should find New Terra, Nexus Station, and New Terra Alpha but not hidden objects
        visible_objects_count = sum(1 for obj in CELESTIAL_OBJECTS 
                                 if not obj["hidden"] and 
                                 obj["coordinates"]["sector"] == "A7" and 
                                 obj["coordinates"]["quadrant"] == "NE")
        self.assertEqual(result.data["count"], visible_objects_count)
        
    def test_scan_region_ultra(self):
        # Test ultra deep scan that should reveal hidden objects
        result = scan_region(
            sector="C5",
            quadrant="NW",
            scan_depth="ultra"
        )
        
        self.assertTrue(result.success)
        # Should find Cerulean Vortex (hidden anomaly)
        expected_count = sum(1 for obj in CELESTIAL_OBJECTS 
                          if obj["coordinates"]["sector"] == "C5" and 
                          obj["coordinates"]["quadrant"] == "NW")
        self.assertEqual(result.data["count"], expected_count)
        
    def test_scan_region_empty(self):
        # Test scanning a region with no objects
        result = scan_region(
            sector="Z1",  # Empty sector
            quadrant="NE",
            scan_depth="standard"
        )
        
        self.assertTrue(result.success)
        self.assertFalse(result.data["found"])
        self.assertEqual(result.data["count"], 0)
        
    def test_scan_region_invalid_parameters(self):
        # Test scanning with invalid parameters
        result = scan_region(
            sector="A7",
            quadrant="INVALID",
            scan_depth="standard"
        )
        
        self.assertFalse(result.success)
        self.assertIn("Invalid quadrant", result.error)

if __name__ == '__main__':
    unittest.main()