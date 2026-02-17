"""
Soil Reporter Module
Generates comprehensive soil analysis reports.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from .soil_sample import SoilSample


class SoilReporter:
    """
    Generates reports from soil analysis and recommendations.
    """
    
    def __init__(self):
        """Initialize the reporter."""
        self.reports_generated = 0
    
    def generate_report(
        self,
        sample: SoilSample,
        recommendation: Optional[Dict] = None,
        format: str = 'text'
    ) -> str:
        """
        Generate a comprehensive soil analysis report.
        
        Args:
            sample: Analyzed soil sample
            recommendation: Optional fertilizer recommendation data
            format: Output format ('text', 'json', 'html')
            
        Returns:
            Formatted report string
        """
        if format == 'json':
            return self._generate_json_report(sample, recommendation)
        elif format == 'html':
            return self._generate_html_report(sample, recommendation)
        else:
            return self._generate_text_report(sample, recommendation)
    
    def _generate_text_report(
        self,
        sample: SoilSample,
        recommendation: Optional[Dict]
    ) -> str:
        """Generate a text-based report."""
        lines = []
        lines.append("=" * 80)
        lines.append("INSOIL TOOL - SOIL ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Sample information
        lines.append("SAMPLE INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Sample ID:        {sample.sample_id}")
        lines.append(f"Location:         {sample.location}")
        lines.append(f"Sampling Depth:   {sample.depth_cm} cm")
        lines.append(f"Collection Date:  {sample.timestamp}")
        if sample.analyzed:
            lines.append(f"Analysis Date:    {sample.analysis_timestamp}")
        lines.append("")
        
        # Nutrient analysis
        if sample.analyzed:
            lines.append("NUTRIENT ANALYSIS")
            lines.append("-" * 80)
            lines.append(f"Nitrogen (N):         {sample.nitrogen:>10.2f} mg/kg")
            lines.append(f"Phosphorus (P):       {sample.phosphorus:>10.2f} mg/kg")
            lines.append(f"Potassium (K):        {sample.potassium:>10.2f} mg/kg")
            lines.append(f"pH:                   {sample.ph:>10.2f}")
            lines.append(f"Organic Carbon:       {sample.organic_carbon:>10.2f} %")
            
            if sample.calcium is not None:
                lines.append("")
                lines.append("MICRONUTRIENTS")
                lines.append("-" * 80)
                lines.append(f"Calcium (Ca):         {sample.calcium:>10.2f} mg/kg")
                lines.append(f"Magnesium (Mg):       {sample.magnesium:>10.2f} mg/kg")
                lines.append(f"Sulfur (S):           {sample.sulfur:>10.2f} mg/kg")
            
            lines.append("")
        
        # Soil texture
        if sample.sand_percent is not None:
            lines.append("SOIL TEXTURE")
            lines.append("-" * 80)
            lines.append(f"Sand:                 {sample.sand_percent:>10.1f} %")
            lines.append(f"Silt:                 {sample.silt_percent:>10.1f} %")
            lines.append(f"Clay:                 {sample.clay_percent:>10.1f} %")
            lines.append(f"Texture Class:        {sample.get_texture_class()}")
            lines.append("")
        
        # Recommendations
        if recommendation:
            lines.append("FERTILIZER RECOMMENDATIONS")
            lines.append("-" * 80)
            lines.append(f"Target Crop:          {recommendation['crop'].title()}")
            lines.append(f"Field Size:           {recommendation['field_size_ha']} hectares")
            lines.append(f"Priority:             {recommendation['priority'].upper()}")
            lines.append("")
            
            # Nutrient status
            lines.append("NUTRIENT STATUS:")
            for nutrient, status in recommendation['nutrient_status'].items():
                status_str = status['status'].upper()
                lines.append(f"  {nutrient.title():20s}: {status_str}")
            lines.append("")
            
            # Fertilizers
            if recommendation['fertilizers']:
                lines.append("RECOMMENDED FERTILIZERS:")
                for i, fert in enumerate(recommendation['fertilizers'], 1):
                    lines.append(f"\n  {i}. {fert['fertilizer']}")
                    lines.append(f"     Rate: {fert['rate_kg_per_ha']} kg/ha")
                    lines.append(f"     Total: {fert['total_kg']} kg for {recommendation['field_size_ha']} ha")
                    lines.append(f"     Timing: {fert['application_timing']}")
                    if 'note' in fert:
                        lines.append(f"     Note: {fert['note']}")
                lines.append("")
            
            # Amendments
            if recommendation['amendments']:
                lines.append("SOIL AMENDMENTS:")
                for i, amend in enumerate(recommendation['amendments'], 1):
                    lines.append(f"\n  {i}. {amend['amendment']}")
                    lines.append(f"     Rate: {amend['rate_kg_per_ha']} kg/ha")
                    lines.append(f"     Purpose: {amend['purpose']}")
                    lines.append(f"     Application: {amend['application']}")
                    if 'benefits' in amend:
                        lines.append(f"     Benefits: {amend['benefits']}")
                lines.append("")
            
            # Cost estimate
            lines.append(f"ESTIMATED COST:       ${recommendation['cost_estimate_usd']:.2f} USD")
            lines.append("")
            
            # Notes
            if recommendation['notes']:
                lines.append("ADDITIONAL NOTES:")
                for note in recommendation['notes']:
                    lines.append(f"  • {note}")
                lines.append("")
        
        lines.append("=" * 80)
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        
        self.reports_generated += 1
        return "\n".join(lines)
    
    def _generate_json_report(
        self,
        sample: SoilSample,
        recommendation: Optional[Dict]
    ) -> str:
        """Generate a JSON report."""
        report = {
            'report_type': 'soil_analysis',
            'generated_at': datetime.now().isoformat(),
            'sample': sample.to_dict(),
            'recommendation': recommendation
        }
        
        self.reports_generated += 1
        return json.dumps(report, indent=2)
    
    def _generate_html_report(
        self,
        sample: SoilSample,
        recommendation: Optional[Dict]
    ) -> str:
        """Generate an HTML report."""
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("  <title>Insoil Tool - Soil Analysis Report</title>")
        html.append("  <style>")
        html.append("    body { font-family: Arial, sans-serif; margin: 40px; }")
        html.append("    h1 { color: #2c5f2d; border-bottom: 3px solid #97bc62; }")
        html.append("    h2 { color: #2c5f2d; border-bottom: 2px solid #97bc62; margin-top: 30px; }")
        html.append("    table { border-collapse: collapse; width: 100%; margin: 20px 0; }")
        html.append("    th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }")
        html.append("    th { background-color: #2c5f2d; color: white; }")
        html.append("    .deficient { color: #d32f2f; font-weight: bold; }")
        html.append("    .adequate { color: #388e3c; font-weight: bold; }")
        html.append("    .excess { color: #f57c00; font-weight: bold; }")
        html.append("    .note { background-color: #fff9c4; padding: 10px; margin: 10px 0; border-left: 4px solid #fbc02d; }")
        html.append("  </style>")
        html.append("</head>")
        html.append("<body>")
        
        html.append("  <h1>INSOIL TOOL - Soil Analysis Report</h1>")
        
        # Sample information
        html.append("  <h2>Sample Information</h2>")
        html.append("  <table>")
        html.append(f"    <tr><td><strong>Sample ID</strong></td><td>{sample.sample_id}</td></tr>")
        html.append(f"    <tr><td><strong>Location</strong></td><td>{sample.location}</td></tr>")
        html.append(f"    <tr><td><strong>Sampling Depth</strong></td><td>{sample.depth_cm} cm</td></tr>")
        html.append(f"    <tr><td><strong>Collection Date</strong></td><td>{sample.timestamp}</td></tr>")
        if sample.analyzed:
            html.append(f"    <tr><td><strong>Analysis Date</strong></td><td>{sample.analysis_timestamp}</td></tr>")
        html.append("  </table>")
        
        # Nutrient analysis
        if sample.analyzed:
            html.append("  <h2>Nutrient Analysis</h2>")
            html.append("  <table>")
            html.append("    <tr><th>Nutrient</th><th>Value</th><th>Unit</th></tr>")
            html.append(f"    <tr><td>Nitrogen (N)</td><td>{sample.nitrogen:.2f}</td><td>mg/kg</td></tr>")
            html.append(f"    <tr><td>Phosphorus (P)</td><td>{sample.phosphorus:.2f}</td><td>mg/kg</td></tr>")
            html.append(f"    <tr><td>Potassium (K)</td><td>{sample.potassium:.2f}</td><td>mg/kg</td></tr>")
            html.append(f"    <tr><td>pH</td><td>{sample.ph:.2f}</td><td>-</td></tr>")
            html.append(f"    <tr><td>Organic Carbon</td><td>{sample.organic_carbon:.2f}</td><td>%</td></tr>")
            html.append("  </table>")
        
        # Recommendations
        if recommendation:
            html.append("  <h2>Fertilizer Recommendations</h2>")
            html.append(f"  <p><strong>Target Crop:</strong> {recommendation['crop'].title()}</p>")
            html.append(f"  <p><strong>Field Size:</strong> {recommendation['field_size_ha']} hectares</p>")
            html.append(f"  <p><strong>Priority:</strong> {recommendation['priority'].upper()}</p>")
            
            # Nutrient status
            html.append("  <h3>Nutrient Status</h3>")
            html.append("  <table>")
            html.append("    <tr><th>Nutrient</th><th>Status</th><th>Details</th></tr>")
            for nutrient, status in recommendation['nutrient_status'].items():
                status_class = status['status']
                status_str = status['status'].upper()
                details = f"Current: {status.get('current', 'N/A')}"
                html.append(f"    <tr><td>{nutrient.title()}</td><td class='{status_class}'>{status_str}</td><td>{details}</td></tr>")
            html.append("  </table>")
            
            # Cost
            html.append(f"  <p><strong>Estimated Cost:</strong> ${recommendation['cost_estimate_usd']:.2f} USD</p>")
        
        html.append(f"  <p><em>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>")
        html.append("</body>")
        html.append("</html>")
        
        self.reports_generated += 1
        return "\n".join(html)
    
    def batch_report(
        self,
        samples: List[SoilSample],
        recommendations: Optional[List[Dict]] = None,
        format: str = 'text'
    ) -> str:
        """
        Generate a batch report for multiple samples.
        
        Args:
            samples: List of soil samples
            recommendations: Optional list of recommendations
            format: Output format
            
        Returns:
            Formatted batch report
        """
        if format == 'json':
            reports = []
            for i, sample in enumerate(samples):
                rec = recommendations[i] if recommendations and i < len(recommendations) else None
                report_data = {
                    'sample': sample.to_dict(),
                    'recommendation': rec
                }
                reports.append(report_data)
            
            return json.dumps({
                'batch_report': True,
                'total_samples': len(samples),
                'generated_at': datetime.now().isoformat(),
                'reports': reports
            }, indent=2)
        else:
            # Text format batch report
            reports = []
            for i, sample in enumerate(samples):
                rec = recommendations[i] if recommendations and i < len(recommendations) else None
                reports.append(self._generate_text_report(sample, rec))
            
            return "\n\n\n".join(reports)
    
    def export_to_file(
        self,
        report: str,
        filename: str
    ):
        """
        Export report to a file.
        
        Args:
            report: Report content
            filename: Output filename
        """
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"Report exported to: {filename}")
    
    def get_stats(self) -> Dict:
        """
        Get reporter statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'reports_generated': self.reports_generated
        }
