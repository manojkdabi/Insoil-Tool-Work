"""
Fertilizer Recommender Module
Provides AI-powered fertilizer and soil amendment recommendations.
"""

from typing import Dict, List, Optional
from .soil_sample import SoilSample


class FertilizerRecommender:
    """
    Generates fertilizer recommendations based on soil analysis and crop requirements.
    """
    
    # Optimal nutrient ranges for common crops (mg/kg or ppm)
    CROP_REQUIREMENTS = {
        'wheat': {
            'nitrogen': (80, 120),
            'phosphorus': (30, 50),
            'potassium': (150, 250),
            'ph': (6.0, 7.5),
            'organic_carbon': (1.5, 3.0)
        },
        'rice': {
            'nitrogen': (100, 150),
            'phosphorus': (25, 45),
            'potassium': (120, 200),
            'ph': (5.5, 6.5),
            'organic_carbon': (2.0, 4.0)
        },
        'corn': {
            'nitrogen': (120, 180),
            'phosphorus': (40, 60),
            'potassium': (150, 300),
            'ph': (6.0, 7.0),
            'organic_carbon': (2.0, 3.5)
        },
        'soybean': {
            'nitrogen': (40, 70),
            'phosphorus': (35, 55),
            'potassium': (150, 250),
            'ph': (6.0, 7.0),
            'organic_carbon': (2.0, 3.5)
        },
        'potato': {
            'nitrogen': (100, 140),
            'phosphorus': (40, 70),
            'potassium': (200, 350),
            'ph': (5.0, 6.5),
            'organic_carbon': (2.5, 4.0)
        },
        'vegetables': {
            'nitrogen': (90, 130),
            'phosphorus': (40, 60),
            'potassium': (150, 250),
            'ph': (6.0, 7.0),
            'organic_carbon': (2.5, 4.0)
        }
    }
    
    def __init__(self):
        """Initialize the recommender."""
        self.recommendation_history = []
    
    def recommend(
        self,
        sample: SoilSample,
        crop: str = 'wheat',
        field_size_ha: float = 1.0
    ) -> Dict:
        """
        Generate fertilizer recommendations for a soil sample.
        
        Args:
            sample: Analyzed SoilSample
            crop: Target crop type
            field_size_ha: Field size in hectares
            
        Returns:
            Dictionary containing recommendations
        """
        if not sample.analyzed:
            raise ValueError("Sample must be analyzed before generating recommendations")
        
        crop = crop.lower()
        if crop not in self.CROP_REQUIREMENTS:
            crop = 'wheat'  # Default to wheat
        
        requirements = self.CROP_REQUIREMENTS[crop]
        
        # Analyze nutrient deficiencies and excesses
        analysis = self._analyze_nutrient_status(sample, requirements)
        
        # Generate fertilizer recommendations
        fertilizers = self._recommend_fertilizers(analysis, field_size_ha)
        
        # Generate soil amendment recommendations
        amendments = self._recommend_amendments(sample, requirements)
        
        # Calculate costs (estimated)
        cost_estimate = self._estimate_costs(fertilizers, amendments)
        
        recommendation = {
            'sample_id': sample.sample_id,
            'crop': crop,
            'field_size_ha': field_size_ha,
            'nutrient_status': analysis,
            'fertilizers': fertilizers,
            'amendments': amendments,
            'cost_estimate_usd': cost_estimate,
            'priority': self._assess_priority(analysis),
            'notes': self._generate_notes(sample, analysis, requirements)
        }
        
        self.recommendation_history.append(recommendation)
        return recommendation
    
    def _analyze_nutrient_status(
        self,
        sample: SoilSample,
        requirements: Dict
    ) -> Dict:
        """
        Analyze nutrient status relative to crop requirements.
        
        Args:
            sample: Soil sample
            requirements: Crop nutrient requirements
            
        Returns:
            Dictionary of nutrient status
        """
        status = {}
        
        nutrients = {
            'nitrogen': sample.nitrogen,
            'phosphorus': sample.phosphorus,
            'potassium': sample.potassium,
            'ph': sample.ph,
            'organic_carbon': sample.organic_carbon
        }
        
        for nutrient, value in nutrients.items():
            if value is None:
                status[nutrient] = {'status': 'unknown', 'deficit': 0}
                continue
            
            min_req, max_req = requirements[nutrient]
            
            if value < min_req:
                deficit = min_req - value
                status[nutrient] = {
                    'status': 'deficient',
                    'current': value,
                    'target': min_req,
                    'deficit': round(deficit, 2)
                }
            elif value > max_req:
                status[nutrient] = {
                    'status': 'excess',
                    'current': value,
                    'target': max_req,
                    'excess': round(value - max_req, 2)
                }
            else:
                status[nutrient] = {
                    'status': 'adequate',
                    'current': value,
                    'target_range': (min_req, max_req)
                }
        
        return status
    
    def _recommend_fertilizers(
        self,
        analysis: Dict,
        field_size_ha: float
    ) -> List[Dict]:
        """
        Recommend specific fertilizers based on deficiencies.
        
        Args:
            analysis: Nutrient status analysis
            field_size_ha: Field size in hectares
            
        Returns:
            List of fertilizer recommendations
        """
        recommendations = []
        
        # Nitrogen recommendations
        if analysis['nitrogen']['status'] == 'deficient':
            deficit = analysis['nitrogen']['deficit']
            # Urea (46% N) application rate
            urea_kg_per_ha = (deficit * 2.17) * 1.1  # 10% buffer
            recommendations.append({
                'fertilizer': 'Urea (46-0-0)',
                'rate_kg_per_ha': round(urea_kg_per_ha, 2),
                'total_kg': round(urea_kg_per_ha * field_size_ha, 2),
                'nutrient_supplied': 'Nitrogen',
                'application_timing': 'Split application: 50% at planting, 50% at growth stage'
            })
        
        # Phosphorus recommendations
        if analysis['phosphorus']['status'] == 'deficient':
            deficit = analysis['phosphorus']['deficit']
            # Triple superphosphate (46% P2O5) 
            tsp_kg_per_ha = (deficit * 2.29) * 1.1
            recommendations.append({
                'fertilizer': 'Triple Superphosphate (0-46-0)',
                'rate_kg_per_ha': round(tsp_kg_per_ha, 2),
                'total_kg': round(tsp_kg_per_ha * field_size_ha, 2),
                'nutrient_supplied': 'Phosphorus',
                'application_timing': 'Apply at planting, incorporate into soil'
            })
        
        # Potassium recommendations
        if analysis['potassium']['status'] == 'deficient':
            deficit = analysis['potassium']['deficit']
            # Muriate of potash (60% K2O)
            mop_kg_per_ha = (deficit * 1.2) * 1.1
            recommendations.append({
                'fertilizer': 'Muriate of Potash (0-0-60)',
                'rate_kg_per_ha': round(mop_kg_per_ha, 2),
                'total_kg': round(mop_kg_per_ha * field_size_ha, 2),
                'nutrient_supplied': 'Potassium',
                'application_timing': 'Apply at planting or early growth'
            })
        
        # NPK complex fertilizer if multiple deficiencies
        if (analysis['nitrogen']['status'] == 'deficient' and 
            analysis['phosphorus']['status'] == 'deficient' and 
            analysis['potassium']['status'] == 'deficient'):
            recommendations.append({
                'fertilizer': 'NPK Complex (20-20-20)',
                'rate_kg_per_ha': 200,
                'total_kg': round(200 * field_size_ha, 2),
                'nutrient_supplied': 'N-P-K',
                'application_timing': 'Apply at planting as base fertilizer',
                'note': 'Can be used as alternative to single-nutrient fertilizers'
            })
        
        return recommendations
    
    def _recommend_amendments(
        self,
        sample: SoilSample,
        requirements: Dict
    ) -> List[Dict]:
        """
        Recommend soil amendments for pH and organic matter.
        
        Args:
            sample: Soil sample
            requirements: Crop requirements
            
        Returns:
            List of amendment recommendations
        """
        amendments = []
        
        # pH amendments
        if sample.ph is not None:
            target_ph = sum(requirements['ph']) / 2
            
            if sample.ph < requirements['ph'][0]:
                # Acidic soil - recommend lime
                ph_diff = target_ph - sample.ph
                lime_kg_per_ha = ph_diff * 1000  # Rough estimate
                amendments.append({
                    'amendment': 'Agricultural Lime (CaCO3)',
                    'rate_kg_per_ha': round(lime_kg_per_ha, 2),
                    'purpose': f'Raise pH from {sample.ph} to {target_ph}',
                    'application': 'Broadcast and incorporate 2-3 months before planting'
                })
            
            elif sample.ph > requirements['ph'][1]:
                # Alkaline soil - recommend sulfur
                ph_diff = sample.ph - target_ph
                sulfur_kg_per_ha = ph_diff * 200
                amendments.append({
                    'amendment': 'Elemental Sulfur',
                    'rate_kg_per_ha': round(sulfur_kg_per_ha, 2),
                    'purpose': f'Lower pH from {sample.ph} to {target_ph}',
                    'application': 'Apply and incorporate several months before planting'
                })
        
        # Organic matter amendments
        if sample.organic_carbon is not None:
            if sample.organic_carbon < requirements['organic_carbon'][0]:
                amendments.append({
                    'amendment': 'Compost or Well-rotted Manure',
                    'rate_kg_per_ha': 5000,
                    'purpose': 'Increase organic matter content',
                    'application': 'Apply and incorporate before planting season',
                    'benefits': 'Improves soil structure, water retention, and nutrient availability'
                })
        
        return amendments
    
    def _estimate_costs(
        self,
        fertilizers: List[Dict],
        amendments: List[Dict]
    ) -> float:
        """
        Estimate total cost of recommendations.
        
        Args:
            fertilizers: List of fertilizer recommendations
            amendments: List of amendment recommendations
            
        Returns:
            Estimated cost in USD
        """
        # Estimated fertilizer prices (USD per kg)
        prices = {
            'Urea (46-0-0)': 0.45,
            'Triple Superphosphate (0-46-0)': 0.60,
            'Muriate of Potash (0-0-60)': 0.55,
            'NPK Complex (20-20-20)': 0.50,
            'Agricultural Lime (CaCO3)': 0.10,
            'Elemental Sulfur': 0.40,
            'Compost or Well-rotted Manure': 0.05
        }
        
        total_cost = 0.0
        
        for fert in fertilizers:
            fertilizer_name = fert['fertilizer']
            if fertilizer_name in prices:
                total_cost += fert['total_kg'] * prices[fertilizer_name]
        
        for amend in amendments:
            amendment_name = amend['amendment']
            if amendment_name in prices:
                total_cost += amend['rate_kg_per_ha'] * prices[amendment_name]
        
        return round(total_cost, 2)
    
    def _assess_priority(self, analysis: Dict) -> str:
        """
        Assess the priority level of recommendations.
        
        Args:
            analysis: Nutrient status analysis
            
        Returns:
            Priority level ('high', 'medium', 'low')
        """
        deficiency_count = sum(
            1 for nutrient_info in analysis.values()
            if nutrient_info.get('status') == 'deficient'
        )
        
        if deficiency_count >= 3:
            return 'high'
        elif deficiency_count >= 1:
            return 'medium'
        else:
            return 'low'
    
    def _generate_notes(
        self,
        sample: SoilSample,
        analysis: Dict,
        requirements: Dict
    ) -> List[str]:
        """
        Generate additional notes and recommendations.
        
        Args:
            sample: Soil sample
            analysis: Nutrient analysis
            requirements: Crop requirements
            
        Returns:
            List of note strings
        """
        notes = []
        
        # Texture-specific notes
        texture_class = sample.get_texture_class()
        if texture_class == "Sandy Loam":
            notes.append("Sandy soil: Apply fertilizers in split doses to reduce leaching losses")
        elif texture_class == "Clay":
            notes.append("Clay soil: Ensure good drainage; consider organic matter addition")
        
        # pH-specific notes
        if sample.ph and sample.ph < 5.5:
            notes.append("Low pH may limit nutrient availability; lime application is strongly recommended")
        elif sample.ph and sample.ph > 7.5:
            notes.append("High pH may reduce micronutrient availability; monitor for deficiencies")
        
        # Organic carbon notes
        if sample.organic_carbon and sample.organic_carbon < 1.5:
            notes.append("Low organic matter: Consider cover cropping and organic amendments")
        
        # General recommendations
        notes.append("Soil test every 2-3 years to monitor nutrient levels")
        notes.append("Follow recommended application rates to avoid environmental pollution")
        
        return notes
    
    def get_recommendations_summary(self) -> Dict:
        """
        Get summary of all recommendations made.
        
        Returns:
            Summary statistics
        """
        return {
            'total_recommendations': len(self.recommendation_history),
            'crops_analyzed': list(set(r['crop'] for r in self.recommendation_history))
        }
