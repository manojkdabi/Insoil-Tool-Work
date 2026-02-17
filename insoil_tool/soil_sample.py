"""
Soil Sample Data Model
Represents a soil sample with its properties and measurements.
"""

import json
from datetime import datetime
from typing import Dict, Optional


class SoilSample:
    """Represents a soil sample with nutrient and property measurements."""
    
    def __init__(
        self,
        sample_id: str,
        location: str,
        depth_cm: float = 15.0,
        timestamp: Optional[str] = None
    ):
        """
        Initialize a soil sample.
        
        Args:
            sample_id: Unique identifier for the sample
            location: Geographic location or field name
            depth_cm: Sampling depth in centimeters (default: 15cm)
            timestamp: Sample collection timestamp (ISO format)
        """
        self.sample_id = sample_id
        self.location = location
        self.depth_cm = depth_cm
        self.timestamp = timestamp or datetime.now().isoformat()
        
        # Nutrient measurements (in mg/kg or ppm)
        self.nitrogen = None  # N
        self.phosphorus = None  # P
        self.potassium = None  # K
        self.organic_carbon = None  # Organic C percentage
        self.ph = None  # pH value (0-14)
        
        # Additional micronutrients
        self.calcium = None  # Ca
        self.magnesium = None  # Mg
        self.sulfur = None  # S
        
        # Soil texture
        self.sand_percent = None
        self.silt_percent = None
        self.clay_percent = None
        
        # Analysis metadata
        self.analyzed = False
        self.analysis_timestamp = None
    
    def set_nutrients(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float,
        organic_carbon: float
    ):
        """
        Set primary nutrient measurements.
        
        Args:
            nitrogen: Nitrogen content (mg/kg)
            phosphorus: Phosphorus content (mg/kg)
            potassium: Potassium content (mg/kg)
            ph: pH value
            organic_carbon: Organic carbon percentage
        """
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.ph = ph
        self.organic_carbon = organic_carbon
        self.analyzed = True
        self.analysis_timestamp = datetime.now().isoformat()
    
    def set_micronutrients(
        self,
        calcium: Optional[float] = None,
        magnesium: Optional[float] = None,
        sulfur: Optional[float] = None
    ):
        """
        Set micronutrient measurements.
        
        Args:
            calcium: Calcium content (mg/kg)
            magnesium: Magnesium content (mg/kg)
            sulfur: Sulfur content (mg/kg)
        """
        self.calcium = calcium
        self.magnesium = magnesium
        self.sulfur = sulfur
    
    def set_texture(
        self,
        sand_percent: float,
        silt_percent: float,
        clay_percent: float
    ):
        """
        Set soil texture composition.
        
        Args:
            sand_percent: Sand percentage
            silt_percent: Silt percentage
            clay_percent: Clay percentage
        """
        if abs((sand_percent + silt_percent + clay_percent) - 100.0) > 0.1:
            raise ValueError("Texture percentages must sum to 100")
        
        self.sand_percent = sand_percent
        self.silt_percent = silt_percent
        self.clay_percent = clay_percent
    
    def get_texture_class(self) -> str:
        """
        Determine soil texture class based on composition.
        
        Returns:
            Soil texture classification
        """
        if not all([self.sand_percent, self.silt_percent, self.clay_percent]):
            return "Unknown"
        
        clay = self.clay_percent
        sand = self.sand_percent
        silt = self.silt_percent
        
        # Simplified USDA texture classification
        if clay >= 40:
            return "Clay"
        elif clay >= 27 and sand <= 45:
            return "Clay Loam"
        elif clay >= 27 and sand > 45:
            return "Sandy Clay"
        elif clay < 27 and sand >= 70:
            return "Sandy Loam"
        elif clay < 27 and silt >= 50:
            return "Silt Loam"
        else:
            return "Loam"
    
    def to_dict(self) -> Dict:
        """
        Convert sample to dictionary format.
        
        Returns:
            Dictionary representation of the sample
        """
        return {
            'sample_id': self.sample_id,
            'location': self.location,
            'depth_cm': self.depth_cm,
            'timestamp': self.timestamp,
            'nutrients': {
                'nitrogen': self.nitrogen,
                'phosphorus': self.phosphorus,
                'potassium': self.potassium,
                'organic_carbon': self.organic_carbon,
                'ph': self.ph,
                'calcium': self.calcium,
                'magnesium': self.magnesium,
                'sulfur': self.sulfur
            },
            'texture': {
                'sand_percent': self.sand_percent,
                'silt_percent': self.silt_percent,
                'clay_percent': self.clay_percent,
                'class': self.get_texture_class()
            },
            'analyzed': self.analyzed,
            'analysis_timestamp': self.analysis_timestamp
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert sample to JSON string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SoilSample':
        """
        Create SoilSample from dictionary.
        
        Args:
            data: Dictionary containing sample data
            
        Returns:
            SoilSample instance
        """
        sample = cls(
            sample_id=data['sample_id'],
            location=data['location'],
            depth_cm=data.get('depth_cm', 15.0),
            timestamp=data.get('timestamp')
        )
        
        nutrients = data.get('nutrients', {})
        if nutrients.get('nitrogen') is not None:
            sample.set_nutrients(
                nitrogen=nutrients['nitrogen'],
                phosphorus=nutrients['phosphorus'],
                potassium=nutrients['potassium'],
                ph=nutrients['ph'],
                organic_carbon=nutrients['organic_carbon']
            )
        
        sample.set_micronutrients(
            calcium=nutrients.get('calcium'),
            magnesium=nutrients.get('magnesium'),
            sulfur=nutrients.get('sulfur')
        )
        
        texture = data.get('texture', {})
        if texture.get('sand_percent') is not None:
            sample.set_texture(
                sand_percent=texture['sand_percent'],
                silt_percent=texture['silt_percent'],
                clay_percent=texture['clay_percent']
            )
        
        return sample
    
    def __repr__(self) -> str:
        """String representation of the sample."""
        status = "Analyzed" if self.analyzed else "Not analyzed"
        return f"SoilSample(id={self.sample_id}, location={self.location}, status={status})"
