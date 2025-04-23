#!/usr/bin/env python3
"""
Command-line interface for RideCo Risk Analysis
"""

import argparse
import json
import sys
import os
from .risk_analysis import (
    compute_risk_with_ranges, 
    visualize_risk_results, 
    perform_sensitivity_analysis, 
    save_parameter_summary
)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Perform FAIR risk analysis for RideCo safety features"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to JSON configuration file with parameter ranges",
        default=None
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory to save output files",
        default="output"
    )
    
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating plots (useful for headless servers)"
    )
    
    parser.add_argument(
        "--samples",
        type=int,
        help="Number of Monte Carlo samples",
        default=1000
    )
    
    return parser.parse_args()


def load_config(config_path):
    """Load configuration from JSON file"""
    if config_path is None:
        return None
        
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI"""
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load configuration if provided, otherwise use defaults
    config = load_config(args.config)
    
    # Define baseline parameters (use config if provided)
    baseline_params = {
        'cf_range': {'min': 400000, 'max': 600000},     # Contact frequency range
        'tc_range': {'min': 6.0, 'max': 9.0},           # Threat capability range
        'rs_range': {'min': 4.0, 'max': 6.0},           # Resistance strength range
        'sl_ef_range': {'min': 0.05, 'max': 0.15},      # Secondary loss event frequency range
        'sl_magnitude_range': {'min': 800000, 'max': 1200000},  # Secondary loss magnitude range
        'n_samples': args.samples
    }
    
    if config:
        baseline_params.update(config)
    
    # Save parameter summary
    save_parameter_summary(baseline_params, output_dir=args.output_dir)
    
    # Perform main risk analysis
    print("Computing risk with Monte Carlo simulation...")
    risk_results, risk_samples = compute_risk_with_ranges(**baseline_params)
    
    # Visualize the results
    print("Generating analysis results...")
    show_plots = not args.no_plots
    result_df = visualize_risk_results(
        risk_results, 
        risk_samples, 
        output_dir=args.output_dir,
        show_plots=show_plots
    )
    
    # Perform sensitivity analysis on highest risk feature
    highest_risk_feature = result_df.iloc[0]['Feature']
    print(f"Performing sensitivity analysis on {highest_risk_feature}...")
    sensitivity_results = perform_sensitivity_analysis(
        highest_risk_feature, 
        risk_results, 
        baseline_params,
        output_dir=args.output_dir,
        show_plots=show_plots
    )
    
    print("\nRisk Assessment Summary:")
    print("------------------------")
    print("1. This analysis uses the FAIR (Factor Analysis of Information Risk) methodology")
    print("2. Monte Carlo simulation is used to handle input parameter ranges")
    print("3. The results show expected annual loss for each safety feature")
    print("4. Features with higher risk scores should be prioritized for implementation")
    print("5. Sensitivity analysis shows which factors most influence risk outcomes")
    
    print("\nRecommendations for RideCo Architecture Design:")
    print("---------------------------------------------")
    print("1. Prioritize implementation of the highest risk features")
    print("2. Focus on improving resistance strength for features with high vulnerability")
    print("3. Consider both probability and impact when designing safety systems")
    print("4. Use these results to inform resource allocation in the architecture design")
    print("5. Implement monitoring for early detection of the most common threat events")
    
    print(f"\nAnalysis complete. Results and visualizations saved to the '{args.output_dir}' directory.")


if __name__ == "__main__":
    main()
