"""
Example: Batch Analysis
Demonstrates analyzing multiple samples at once
"""

from insoil_tool import SoilSample, SoilAnalyzer, FertilizerRecommender, SoilReporter


def main():
    print("=" * 80)
    print("EXAMPLE 2: Batch Soil Analysis")
    print("=" * 80)
    print()
    
    # Create multiple samples
    print("Creating multiple soil samples...")
    samples = [
        SoilSample("FIELD001", "North Field", depth_cm=15),
        SoilSample("FIELD002", "South Field", depth_cm=15),
        SoilSample("FIELD003", "East Field", depth_cm=20),
        SoilSample("FIELD004", "West Field", depth_cm=15)
    ]
    
    # Add texture data to some samples
    samples[0].set_texture(40, 35, 25)  # Loam
    samples[1].set_texture(70, 20, 10)  # Sandy Loam
    samples[2].set_texture(20, 30, 50)  # Clay
    
    print(f"Created {len(samples)} samples")
    print()
    
    # Batch analyze
    print("Performing batch analysis...")
    analyzer = SoilAnalyzer()
    analyzed_samples = analyzer.batch_analyze(samples, quick_mode=False)
    print(f"✓ Analyzed {len(analyzed_samples)} samples")
    print()
    
    # Generate recommendations for each
    print("Generating recommendations...")
    recommender = FertilizerRecommender()
    recommendations = []
    
    crops = ['wheat', 'rice', 'corn', 'soybean']
    for i, sample in enumerate(analyzed_samples):
        crop = crops[i % len(crops)]
        rec = recommender.recommend(sample, crop=crop, field_size_ha=1.0)
        recommendations.append(rec)
        print(f"  {sample.sample_id}: {crop} - Priority: {rec['priority']}")
    print()
    
    # Generate batch report
    print("Generating batch report...")
    reporter = SoilReporter()
    
    # Summary
    print("\nSample Summary:")
    print("-" * 80)
    for sample, rec in zip(analyzed_samples, recommendations):
        texture = sample.get_texture_class()
        print(f"{sample.sample_id:12s} | pH: {sample.ph:4.1f} | "
              f"N: {sample.nitrogen:6.1f} | P: {sample.phosphorus:6.1f} | "
              f"K: {sample.potassium:6.1f} | Texture: {texture:12s}")
    print()
    
    # Generate JSON batch report
    json_report = reporter.batch_report(analyzed_samples, recommendations, format='json')
    reporter.export_to_file(json_report, '/tmp/batch_report.json')
    print("✓ Batch report exported to /tmp/batch_report.json")
    
    # Statistics
    print("\nAnalysis Statistics:")
    print(f"  Total samples analyzed: {len(analyzed_samples)}")
    print(f"  Analyzer stats: {analyzer.get_analysis_stats()}")
    print(f"  Reporter stats: {reporter.get_stats()}")


if __name__ == '__main__':
    main()
