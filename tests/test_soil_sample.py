"""
Unit tests for SoilSample class
"""

import unittest
import json
from insoil_tool.soil_sample import SoilSample


class TestSoilSample(unittest.TestCase):
    """Test cases for SoilSample class."""
    
    def test_create_sample(self):
        """Test creating a basic soil sample."""
        sample = SoilSample(
            sample_id="TEST001",
            location="Test Field",
            depth_cm=15.0
        )
        
        self.assertEqual(sample.sample_id, "TEST001")
        self.assertEqual(sample.location, "Test Field")
        self.assertEqual(sample.depth_cm, 15.0)
        self.assertFalse(sample.analyzed)
    
    def test_set_nutrients(self):
        """Test setting nutrient values."""
        sample = SoilSample("TEST002", "Test Field")
        sample.set_nutrients(
            nitrogen=100.0,
            phosphorus=40.0,
            potassium=200.0,
            ph=6.5,
            organic_carbon=2.5
        )
        
        self.assertEqual(sample.nitrogen, 100.0)
        self.assertEqual(sample.phosphorus, 40.0)
        self.assertEqual(sample.potassium, 200.0)
        self.assertEqual(sample.ph, 6.5)
        self.assertEqual(sample.organic_carbon, 2.5)
        self.assertTrue(sample.analyzed)
    
    def test_set_texture(self):
        """Test setting soil texture."""
        sample = SoilSample("TEST003", "Test Field")
        sample.set_texture(
            sand_percent=40.0,
            silt_percent=35.0,
            clay_percent=25.0
        )
        
        self.assertEqual(sample.sand_percent, 40.0)
        self.assertEqual(sample.silt_percent, 35.0)
        self.assertEqual(sample.clay_percent, 25.0)
    
    def test_texture_validation(self):
        """Test that texture percentages must sum to 100."""
        sample = SoilSample("TEST004", "Test Field")
        
        with self.assertRaises(ValueError):
            sample.set_texture(
                sand_percent=40.0,
                silt_percent=30.0,
                clay_percent=20.0  # Sum = 90, not 100
            )
    
    def test_get_texture_class(self):
        """Test texture classification."""
        sample = SoilSample("TEST005", "Test Field")
        
        # Test Loam
        sample.set_texture(40, 35, 25)
        self.assertEqual(sample.get_texture_class(), "Loam")
        
        # Test Sandy Loam
        sample.set_texture(70, 20, 10)
        self.assertEqual(sample.get_texture_class(), "Sandy Loam")
        
        # Test Clay
        sample.set_texture(20, 30, 50)
        self.assertEqual(sample.get_texture_class(), "Clay")
    
    def test_to_dict(self):
        """Test converting sample to dictionary."""
        sample = SoilSample("TEST006", "Test Field", depth_cm=20.0)
        sample.set_nutrients(100, 40, 200, 6.5, 2.5)
        
        data = sample.to_dict()
        
        self.assertEqual(data['sample_id'], "TEST006")
        self.assertEqual(data['location'], "Test Field")
        self.assertEqual(data['depth_cm'], 20.0)
        self.assertEqual(data['nutrients']['nitrogen'], 100)
        self.assertTrue(data['analyzed'])
    
    def test_to_json(self):
        """Test converting sample to JSON."""
        sample = SoilSample("TEST007", "Test Field")
        sample.set_nutrients(100, 40, 200, 6.5, 2.5)
        
        json_str = sample.to_json()
        data = json.loads(json_str)
        
        self.assertEqual(data['sample_id'], "TEST007")
        self.assertEqual(data['nutrients']['nitrogen'], 100)
    
    def test_from_dict(self):
        """Test creating sample from dictionary."""
        data = {
            'sample_id': 'TEST008',
            'location': 'Test Field',
            'depth_cm': 15.0,
            'nutrients': {
                'nitrogen': 100,
                'phosphorus': 40,
                'potassium': 200,
                'ph': 6.5,
                'organic_carbon': 2.5
            },
            'texture': {
                'sand_percent': 40,
                'silt_percent': 35,
                'clay_percent': 25
            }
        }
        
        sample = SoilSample.from_dict(data)
        
        self.assertEqual(sample.sample_id, 'TEST008')
        self.assertEqual(sample.nitrogen, 100)
        self.assertEqual(sample.sand_percent, 40)


if __name__ == '__main__':
    unittest.main()
