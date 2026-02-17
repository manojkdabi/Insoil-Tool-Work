"""
Example: Advanced Analysis with Data Persistence
Demonstrates saving and loading soil samples
"""

import json
from insoil_tool import SoilSample, SoilAnalyzer, FertilizerRecommender, SoilReporter


def main():
    print("=" * 80)
    print("EXAMPLE 3: Advanced Analysis with Data Persistence")
    print("=" * 80)
    print()
    
    # Create and analyze a sample
    print("Creating and analyzing sample...")
    sample = SoilSample(
        sample_id="ADV001",
        location="Research Plot 1",
        depth_cm=20.0
    )
    sample.set_texture(sand_percent=35, silt_percent=40, clay_percent=25)
    
    analyzer = SoilAnalyzer(calibration_mode="high_precision")
    sample = analyzer.analyze_sample(sample, quick_mode=False)
    print(f"✓ Sample analyzed: {sample.sample_id}")
    print(f"  Texture: {sample.get_texture_class()}")
    print()
    
    # Save sample to file
    print("Saving sample to JSON file...")
    sample_json = sample.to_json()
    with open('/tmp/sample_adv001.json', 'w') as f:
        f.write(sample_json)
    print("✓ Saved to /tmp/sample_adv001.json")
    print()
    
    # Load sample from file
    print("Loading sample from file...")
    with open('/tmp/sample_adv001.json', 'r') as f:
        loaded_data = json.load(f)
    
    loaded_sample = SoilSample.from_dict(loaded_data)
    print(f"✓ Loaded sample: {loaded_sample.sample_id}")
    print(f"  Location: {loaded_sample.location}")
    print(f"  Analyzed: {loaded_sample.analyzed}")
    print()
    
    # Generate recommendations for different crops
    print("Comparing recommendations for different crops...")
    recommender = FertilizerRecommender()
    crops = ['wheat', 'rice', 'corn', 'potato']
    
    print("\n{:<12s} | {:<8s} | {:>10s} | {:>15s}".format(
        "Crop", "Priority", "Cost (USD)", "Fertilizers"
    ))
    print("-" * 60)
    
    for crop in crops:
        rec = recommender.recommend(loaded_sample, crop=crop, field_size_ha=1.0)
        n_fertilizers = len(rec['fertilizers'])
        print("{:<12s} | {:<8s} | {:>10.2f} | {:>15d}".format(
            crop.title(),
            rec['priority'].upper(),
            rec['cost_estimate_usd'],
            n_fertilizers
        ))
    print()
    
    # Generate HTML report for wheat
    print("Generating HTML report for wheat...")
    rec = recommender.recommend(loaded_sample, crop='wheat', field_size_ha=2.0)
    reporter = SoilReporter()
    html_report = reporter.generate_report(loaded_sample, rec, format='html')
    reporter.export_to_file(html_report, '/tmp/wheat_report.html')
    print("✓ HTML report saved to /tmp/wheat_report.html")
    print()
    
    # Print summary
    print("Summary:")
    print(f"  Recommendations generated: {len(crops)}")
    print(f"  Reports created: {reporter.get_stats()['reports_generated']}")
    print(f"  Recommendation history: {recommender.get_recommendations_summary()}")


if __name__ == '__main__':
    main()
