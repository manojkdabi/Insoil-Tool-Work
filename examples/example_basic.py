"""
Example: Basic Soil Analysis
Demonstrates basic usage of the Insoil Tool
"""

from insoil_tool import SoilSample, SoilAnalyzer, FertilizerRecommender, SoilReporter


def main():
    print("=" * 80)
    print("EXAMPLE 1: Basic Soil Analysis")
    print("=" * 80)
    print()
    
    # Step 1: Create a soil sample
    print("Step 1: Creating soil sample...")
    sample = SoilSample(
        sample_id="SAMPLE001",
        location="North Field, Farm A",
        depth_cm=15.0
    )
    print(f"Created: {sample}")
    print()
    
    # Step 2: Analyze the sample
    print("Step 2: Analyzing soil sample...")
    analyzer = SoilAnalyzer(calibration_mode="standard")
    sample = analyzer.analyze_sample(sample, quick_mode=False)
    print(f"Analysis complete!")
    print(f"  Nitrogen: {sample.nitrogen} mg/kg")
    print(f"  Phosphorus: {sample.phosphorus} mg/kg")
    print(f"  Potassium: {sample.potassium} mg/kg")
    print(f"  pH: {sample.ph}")
    print(f"  Organic Carbon: {sample.organic_carbon}%")
    print()
    
    # Step 3: Generate recommendations
    print("Step 3: Generating fertilizer recommendations...")
    recommender = FertilizerRecommender()
    recommendation = recommender.recommend(
        sample=sample,
        crop='wheat',
        field_size_ha=2.5
    )
    print(f"Recommendations for {recommendation['crop']} ({recommendation['field_size_ha']} ha):")
    print(f"  Priority: {recommendation['priority']}")
    print(f"  Estimated Cost: ${recommendation['cost_estimate_usd']}")
    print()
    
    # Step 4: Generate report
    print("Step 4: Generating report...")
    reporter = SoilReporter()
    report = reporter.generate_report(sample, recommendation, format='text')
    print(report)
    print()
    
    # Export to file
    reporter.export_to_file(report, '/tmp/soil_report.txt')
    print("Report exported to /tmp/soil_report.txt")


if __name__ == '__main__':
    main()
