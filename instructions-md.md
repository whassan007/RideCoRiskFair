# RideCo Safety Risk Analysis Package

This document provides detailed instructions for installing, using, and deploying the RideCo Safety Risk Analysis package.

## Installation

### Option 1: Standard Python Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rideco-safety-risk-analysis.git
   cd rideco-safety-risk-analysis
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

### Option 2: Using Docker

1. Build the Docker image:
   ```bash
   docker build -t rideco-risk-analysis .
   ```

## Usage

### Command Line Interface

The package provides a command-line interface for running the risk analysis:

```bash
# Run with default parameters
rideco-risk-analysis

# Specify an output directory
rideco-risk-analysis --output-dir ./my-results

# Use a custom configuration file
rideco-risk-analysis --config ./config/example_config.json

# Run without generating plots (useful for headless servers)
rideco-risk-analysis --no-plots

# Specify the number of Monte Carlo samples
rideco-risk-analysis --samples 5000
```

### Using Docker

```bash
# Run with default parameters
docker run -v $(pwd)/output:/app/output rideco-risk-analysis

# Use a custom configuration file
docker run -v $(pwd)/output:/app/output -v $(pwd)/config:/app/config rideco-risk-analysis --config /app/config/example_config.json
```

### Using Docker Compose

```bash
# Run the default analysis
docker-compose up rideco-risk-analysis

# Run the headless analysis (no plots)
docker-compose up headless-analysis
```

## Configuration File

The configuration file is a JSON file that specifies parameter ranges for the risk analysis. An example configuration file is provided in `config/example_config.json`.

Example:
```json
{
  "cf_range": {
    "min": 500000,
    "max": 700000
  },
  "tc_range": {
    "min": 7.0, 
    "max": 9.5
  },
  "rs_range": {
    "min": 3.0,
    "max": 5.0
  }
}
```

## Output Files

The analysis generates various output files in the specified output directory:

- `risk_analysis_results.csv`: Results table with risk metrics for each feature
- `rideco_safety_risk_comparison.png`: Boxplot comparison of risk across features
- `rideco_safety_fair_components.png`: Breakdown of FAIR components
- `rideco_safety_risk_distribution.png`: Probability distribution of risk outcomes
- `rideco_safety_risk_heatmap.png`: Heatmap of normalized risk components
- `key_insights.txt`: Summary of key findings
- `parameter_summary.txt`: Summary of input parameters
- `sensitivity_analysis_*.png`: Sensitivity analysis for the highest-risk feature

## Development

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage report
pytest --cov=rideco_risk_analysis
```

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports
isort .
```

### Building the Package

```bash
python -m build
```

## Customizing the Analysis

To add or modify safety features, edit the `features` dictionary in `rideco_risk_analysis/risk_analysis.py` or provide a `features_config` section in your configuration file.