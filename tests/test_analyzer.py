"""
Unit tests for SoilAnalyzer class
"""

import unittest
from insoil_tool.soil_sample import SoilSample
from insoil_tool.analyzer import SoilAnalyzer


class TestSoilAnalyzer(unittest.TestCase):
    """Test cases for SoilAnalyzer class."""
    
    def test_create_analyzer(self):
        """Test creating an analyzer."""
        analyzer = SoilAnalyzer(calibration_mode="standard")
        
        self.assertEqual(analyzer.calibration_mode, "standard")
        self.assertEqual(analyzer.analysis_count, 0)
    
    def test_analyze_sample(self):
        """Test analyzing a soil sample."""
        sample = SoilSample("TEST001", "Test Field")
        analyzer = SoilAnalyzer()
        
        analyzed_sample = analyzer.analyze_sample(sample, quick_mode=False)
        
        self.assertTrue(analyzed_sample.analyzed)
        self.assertIsNotNone(analyzed_sample.nitrogen)
        self.assertIsNotNone(analyzed_sample.phosphorus)
        self.assertIsNotNone(analyzed_sample.potassium)
        self.assertIsNotNone(analyzed_sample.ph)
        self.assertIsNotNone(analyzed_sample.organic_carbon)
        self.assertEqual(analyzer.analysis_count, 1)
    
    def test_quick_mode(self):
        """Test quick analysis mode."""
        sample = SoilSample("TEST002", "Test Field")
        analyzer = SoilAnalyzer()
        
        analyzed_sample = analyzer.analyze_sample(sample, quick_mode=True)
        
        self.assertTrue(analyzed_sample.analyzed)
        # Quick mode doesn't analyze micronutrients
        self.assertIsNone(analyzed_sample.calcium)
    
    def test_batch_analyze(self):
        """Test batch analysis."""
        samples = [
            SoilSample("TEST003", "Field 1"),
            SoilSample("TEST004", "Field 2"),
            SoilSample("TEST005", "Field 3")
        ]
        
        analyzer = SoilAnalyzer()
        analyzed_samples = analyzer.batch_analyze(samples)
        
        self.assertEqual(len(analyzed_samples), 3)
        self.assertEqual(analyzer.analysis_count, 3)
        
        for sample in analyzed_samples:
            self.assertTrue(sample.analyzed)
    
    def test_nutrient_ranges(self):
        """Test that analyzed nutrients are in reasonable ranges."""
        sample = SoilSample("TEST006", "Test Field")
        analyzer = SoilAnalyzer()
        
        analyzed_sample = analyzer.analyze_sample(sample)
        
        # Check ranges
        self.assertGreater(analyzed_sample.nitrogen, 0)
        self.assertLess(analyzed_sample.nitrogen, 500)
        
        self.assertGreater(analyzed_sample.phosphorus, 0)
        self.assertLess(analyzed_sample.phosphorus, 200)
        
        self.assertGreater(analyzed_sample.potassium, 0)
        self.assertLess(analyzed_sample.potassium, 600)
        
        self.assertGreaterEqual(analyzed_sample.ph, 4.0)
        self.assertLessEqual(analyzed_sample.ph, 9.0)
        
        self.assertGreater(analyzed_sample.organic_carbon, 0)
        self.assertLess(analyzed_sample.organic_carbon, 10)
    
    def test_get_analysis_stats(self):
        """Test getting analyzer statistics."""
        analyzer = SoilAnalyzer()
        sample = SoilSample("TEST007", "Test Field")
        analyzer.analyze_sample(sample)
        
        stats = analyzer.get_analysis_stats()
        
        self.assertEqual(stats['total_analyses'], 1)
        self.assertIn('wavelengths', stats)


if __name__ == '__main__':
    unittest.main()
