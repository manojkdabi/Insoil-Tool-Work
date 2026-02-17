"""
Insoil Tool - Soil Testing and Analysis Platform
Provides rapid soil nutrient analysis and AI-powered recommendations.
"""

__version__ = "1.0.0"
__author__ = "Insoil Tool Development Team"

from .soil_sample import SoilSample
from .analyzer import SoilAnalyzer
from .recommender import FertilizerRecommender
from .reporter import SoilReporter

__all__ = [
    'SoilSample',
    'SoilAnalyzer',
    'FertilizerRecommender',
    'SoilReporter'
]
