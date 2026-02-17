# Insoil Tool - Soil Testing and Analysis Platform

A comprehensive Python-based soil analysis tool that provides rapid nutrient analysis and AI-powered fertilizer recommendations for sustainable agriculture.

## Features

- **Rapid Soil Analysis**: Simulates photospectrometry-based soil nutrient detection
- **Comprehensive Nutrient Testing**: Analyzes N, P, K, pH, organic carbon, and micronutrients
- **AI-Powered Recommendations**: Generates crop-specific fertilizer recommendations
- **Multiple Output Formats**: Supports text, JSON, and HTML report generation
- **Batch Processing**: Analyze multiple samples simultaneously
- **Data Persistence**: Save and load sample data in JSON format
- **CLI Interface**: Easy-to-use command-line interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/manojkdabi/Insoil-Tool-Work.git
cd Insoil-Tool-Work
```

2. Install dependencies (optional - for visualization):
```bash
pip install -r requirements.txt
```

## Quick Start

### Using the Command Line Interface

```bash
# Analyze a soil sample
python cli.py analyze --id FIELD001 --location "North Field" --crop wheat --field-size 2.5

# List available crops
python cli.py list-crops

# Generate HTML report
python cli.py analyze --id FIELD002 --location "South Field" --crop rice --format html --output report.html
```

### Using Python API

```python
from insoil_tool import SoilSample, SoilAnalyzer, FertilizerRecommender, SoilReporter

# Create a soil sample
sample = SoilSample(
    sample_id="SAMPLE001",
    location="North Field",
    depth_cm=15.0
)

# Analyze the sample
analyzer = SoilAnalyzer()
sample = analyzer.analyze_sample(sample)

# Generate recommendations
recommender = FertilizerRecommender()
recommendation = recommender.recommend(sample, crop='wheat', field_size_ha=2.0)

# Create a report
reporter = SoilReporter()
report = reporter.generate_report(sample, recommendation)
print(report)
```

## Examples

The `examples/` directory contains three comprehensive examples:

- **example_basic.py**: Basic soil analysis workflow
- **example_batch.py**: Batch processing multiple samples
- **example_advanced.py**: Advanced features with data persistence

Run examples:
```bash
python -m examples.example_basic
python -m examples.example_batch
python -m examples.example_advanced
```

## Supported Crops

- Wheat
- Rice
- Corn
- Soybean
- Potato
- Vegetables

## Module Documentation

### SoilSample
Represents a soil sample with its properties and measurements.
```python
sample = SoilSample(sample_id="ID", location="Location")
sample.set_nutrients(nitrogen=100, phosphorus=40, potassium=200, ph=6.5, organic_carbon=2.5)
sample.set_texture(sand_percent=40, silt_percent=35, clay_percent=25)
```

### SoilAnalyzer
Analyzes soil samples using simulated photospectrometry.
```python
analyzer = SoilAnalyzer(calibration_mode="standard")
analyzed_sample = analyzer.analyze_sample(sample, quick_mode=False)
```

### FertilizerRecommender
Generates AI-powered fertilizer recommendations.
```python
recommender = FertilizerRecommender()
recommendation = recommender.recommend(sample, crop='wheat', field_size_ha=1.0)
```

### SoilReporter
Generates comprehensive reports in multiple formats.
```python
reporter = SoilReporter()
report = reporter.generate_report(sample, recommendation, format='html')
reporter.export_to_file(report, 'report.html')
```

## Project Structure

```
Insoil-Tool-Work/
├── insoil_tool/          # Main package
│   ├── __init__.py       # Package initialization
│   ├── soil_sample.py    # Soil sample data model
│   ├── analyzer.py       # Soil analysis engine
│   ├── recommender.py    # Fertilizer recommendation system
│   └── reporter.py       # Report generation
├── examples/             # Usage examples
├── tests/                # Test suite
├── cli.py                # Command-line interface
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Testing

Run tests (if test suite is implemented):
```bash
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for agricultural development purposes.

## About Insoil Tool

The Insoil Tool is designed to support sustainable agriculture by providing farmers and agricultural professionals with rapid, accurate soil analysis and actionable recommendations. The tool helps optimize fertilizer use, improve crop yields, reduce costs, and support soil health restoration.

## Support

For questions, issues, or suggestions, please open an issue on GitHub.
