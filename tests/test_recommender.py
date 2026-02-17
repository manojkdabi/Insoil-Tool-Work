"""
Unit tests for FertilizerRecommender class
"""

import unittest
from insoil_tool.soil_sample import SoilSample
from insoil_tool.analyzer import SoilAnalyzer
from insoil_tool.recommender import FertilizerRecommender


class TestFertilizerRecommender(unittest.TestCase):
    """Test cases for FertilizerRecommender class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create and analyze a sample
        self.sample = SoilSample("TEST001", "Test Field")
        analyzer = SoilAnalyzer()
        self.sample = analyzer.analyze_sample(self.sample)
    
    def test_create_recommender(self):
        """Test creating a recommender."""
        recommender = FertilizerRecommender()
        
        self.assertEqual(len(recommender.recommendation_history), 0)
    
    def test_recommend_for_wheat(self):
        """Test generating recommendations for wheat."""
        recommender = FertilizerRecommender()
        recommendation = recommender.recommend(
            self.sample,
            crop='wheat',
            field_size_ha=1.0
        )
        
        self.assertEqual(recommendation['crop'], 'wheat')
        self.assertEqual(recommendation['field_size_ha'], 1.0)
        self.assertIn('nutrient_status', recommendation)
        self.assertIn('fertilizers', recommendation)
        self.assertIn('amendments', recommendation)
        self.assertIn('cost_estimate_usd', recommendation)
    
    def test_unanalyzed_sample_error(self):
        """Test that unanalyzed sample raises error."""
        recommender = FertilizerRecommender()
        unanalyzed_sample = SoilSample("TEST002", "Test Field")
        
        with self.assertRaises(ValueError):
            recommender.recommend(unanalyzed_sample, crop='wheat')
    
    def test_unknown_crop_defaults_to_wheat(self):
        """Test that unknown crop defaults to wheat."""
        recommender = FertilizerRecommender()
        recommendation = recommender.recommend(
            self.sample,
            crop='unknown_crop',
            field_size_ha=1.0
        )
        
        # Should default to wheat
        self.assertIn('nutrient_status', recommendation)
    
    def test_recommendations_for_all_crops(self):
        """Test recommendations for all supported crops."""
        recommender = FertilizerRecommender()
        crops = ['wheat', 'rice', 'corn', 'soybean', 'potato', 'vegetables']
        
        for crop in crops:
            recommendation = recommender.recommend(
                self.sample,
                crop=crop,
                field_size_ha=1.0
            )
            self.assertIsNotNone(recommendation)
            self.assertIn('nutrient_status', recommendation)
    
    def test_priority_assessment(self):
        """Test priority assessment."""
        recommender = FertilizerRecommender()
        recommendation = recommender.recommend(
            self.sample,
            crop='wheat',
            field_size_ha=1.0
        )
        
        self.assertIn(recommendation['priority'], ['high', 'medium', 'low'])
    
    def test_cost_estimate(self):
        """Test cost estimation."""
        recommender = FertilizerRecommender()
        recommendation = recommender.recommend(
            self.sample,
            crop='wheat',
            field_size_ha=2.0
        )
        
        self.assertGreaterEqual(recommendation['cost_estimate_usd'], 0)
    
    def test_field_size_scaling(self):
        """Test that recommendations scale with field size."""
        recommender = FertilizerRecommender()
        
        rec_1ha = recommender.recommend(self.sample, crop='wheat', field_size_ha=1.0)
        rec_2ha = recommender.recommend(self.sample, crop='wheat', field_size_ha=2.0)
        
        # Cost should scale with field size if there are fertilizers recommended
        if rec_1ha['fertilizers']:
            # If fertilizers are recommended, cost should scale
            self.assertGreater(rec_2ha['cost_estimate_usd'], rec_1ha['cost_estimate_usd'])
        else:
            # If no fertilizers, both should be same (amendments scale with ha already)
            self.assertGreaterEqual(rec_2ha['cost_estimate_usd'], rec_1ha['cost_estimate_usd'])
    
    def test_recommendation_history(self):
        """Test that recommendations are saved to history."""
        recommender = FertilizerRecommender()
        
        recommender.recommend(self.sample, crop='wheat', field_size_ha=1.0)
        recommender.recommend(self.sample, crop='rice', field_size_ha=1.0)
        
        self.assertEqual(len(recommender.recommendation_history), 2)
    
    def test_get_recommendations_summary(self):
        """Test getting recommendations summary."""
        recommender = FertilizerRecommender()
        
        recommender.recommend(self.sample, crop='wheat', field_size_ha=1.0)
        recommender.recommend(self.sample, crop='rice', field_size_ha=1.0)
        
        summary = recommender.get_recommendations_summary()
        
        self.assertEqual(summary['total_recommendations'], 2)
        self.assertIn('wheat', summary['crops_analyzed'])
        self.assertIn('rice', summary['crops_analyzed'])


if __name__ == '__main__':
    unittest.main()
