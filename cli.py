#!/usr/bin/env python3
"""
Insoil Tool CLI - Command Line Interface for Soil Analysis
"""

import argparse
import sys
from insoil_tool import SoilSample, SoilAnalyzer, FertilizerRecommender, SoilReporter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Insoil Tool - Rapid Soil Analysis and Recommendations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a soil sample
  python cli.py analyze --id FIELD001 --location "North Field" --crop wheat

  # Analyze with texture data
  python cli.py analyze --id FIELD002 --location "South Field" --crop rice --texture 40,35,25

  # Generate report in HTML format
  python cli.py analyze --id FIELD003 --location "East Field" --crop corn --format html --output report.html
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a soil sample')
    analyze_parser.add_argument('--id', required=True, help='Sample ID')
    analyze_parser.add_argument('--location', required=True, help='Sample location or field name')
    analyze_parser.add_argument('--depth', type=float, default=15.0, help='Sampling depth in cm (default: 15)')
    analyze_parser.add_argument('--crop', default='wheat', help='Target crop (default: wheat)')
    analyze_parser.add_argument('--field-size', type=float, default=1.0, help='Field size in hectares (default: 1.0)')
    analyze_parser.add_argument('--texture', help='Soil texture as sand,silt,clay percentages (e.g., 40,35,25)')
    analyze_parser.add_argument('--quick', action='store_true', help='Use quick analysis mode')
    analyze_parser.add_argument('--format', choices=['text', 'json', 'html'], default='text', help='Output format')
    analyze_parser.add_argument('--output', help='Output file (default: print to console)')
    
    # List crops command
    list_parser = subparsers.add_parser('list-crops', help='List available crop types')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        run_analysis(args)
    elif args.command == 'list-crops':
        list_crops()
    else:
        parser.print_help()
        sys.exit(1)


def run_analysis(args):
    """Run soil analysis workflow."""
    print("=" * 80)
    print("INSOIL TOOL - Soil Analysis System")
    print("=" * 80)
    print()
    
    # Create sample
    print(f"Creating sample: {args.id}")
    sample = SoilSample(
        sample_id=args.id,
        location=args.location,
        depth_cm=args.depth
    )
    
    # Set texture if provided
    if args.texture:
        try:
            sand, silt, clay = map(float, args.texture.split(','))
            sample.set_texture(sand, silt, clay)
            print(f"Texture set: {sand}% sand, {silt}% silt, {clay}% clay")
        except Exception as e:
            print(f"Warning: Invalid texture data - {e}")
    
    # Analyze sample
    print(f"Analyzing sample (quick mode: {args.quick})...")
    analyzer = SoilAnalyzer()
    sample = analyzer.analyze_sample(sample, quick_mode=args.quick)
    print("✓ Analysis complete")
    print()
    
    # Generate recommendations
    print(f"Generating recommendations for {args.crop}...")
    recommender = FertilizerRecommender()
    recommendation = recommender.recommend(
        sample,
        crop=args.crop,
        field_size_ha=args.field_size
    )
    print("✓ Recommendations generated")
    print()
    
    # Generate report
    print("Generating report...")
    reporter = SoilReporter()
    report = reporter.generate_report(sample, recommendation, format=args.format)
    
    if args.output:
        reporter.export_to_file(report, args.output)
        print(f"✓ Report saved to: {args.output}")
    else:
        print()
        print(report)


def list_crops():
    """List available crop types."""
    print("Available Crop Types:")
    print("-" * 40)
    recommender = FertilizerRecommender()
    for crop in sorted(recommender.CROP_REQUIREMENTS.keys()):
        print(f"  • {crop}")
    print()


if __name__ == '__main__':
    main()
