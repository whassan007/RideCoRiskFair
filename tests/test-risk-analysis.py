"""
Unit tests for risk analysis module
"""
import pytest
import numpy as np
from rideco_risk_analysis.risk_analysis import (
    logistic_function, 
    sample_from_range,
    compute_risk_with_ranges
)

def test_logistic_function():
    """Test the logistic function used for vulnerability calculation"""
    # Test zero value (should be 0.5)
    assert abs(logistic_function(0) - 0.5) < 1e-10
    
    # Test positive value (should be > 0.5)
    assert logistic_function(2) > 0.5
    
    # Test negative value (should be < 0.5)
    assert logistic_function(-2) < 0.5
    
    # Test extreme values
    assert logistic_function(100) > 0.999
    assert logistic_function(-100) < 0.001


def test_sample_from_range():
    """Test the sampling function for ranges"""
    # Test with min-max dict
    samples = sample_from_range({'min': 1.0, 'max': 5.0}, n_samples=1000)
    
    # Check shape
    assert samples.shape == (1000,)
    
    # Check bounds
    assert np.all(samples >= 1.0)
    assert np.all(samples <= 5.0)
    
    # Test with single value
    samples = sample_from_range(3.0, n_samples=500)
    assert samples.shape == (500,)
    assert np.all(samples == 3.0)


def test_compute_risk_with_ranges():
    """Test the main risk computation function"""
    # Use minimal test parameters
    test_params = {
        'cf_range': {'min': 100, 'max': 200},
        'tc_range': {'min': 5.0, 'max': 6.0},
        'rs_range': {'min': 4.0, 'max': 5.0},
        'sl_ef_range': {'min': 0.1, 'max': 0.2},
        'sl_magnitude_range': {'min': 1000, 'max': 2000},
        'n_samples': 100
    }
    
    # Run computation
    results, risk_samples = compute_risk_with_ranges(**test_params)
    
    # Basic structure checks
    assert isinstance(results, dict)
    assert isinstance(risk_samples, dict)
    
    # Check if all features are included
    assert len(results) >= 9  # At least 9 safety features
    
    # Check structure of results for first feature
    first_feature = list(results.keys())[0]
    for component in ['tef', 'vulnerability', 'lef', 'lm', 'risk']:
        assert component in results[first_feature]
        for stat in ['mean', 'median', 'p5', 'p95']:
            assert stat in results[first_feature][component]
    
    # Check risk values are positive
    for feature in results:
        assert results[feature]['risk']['median'] > 0


if __name__ == "__main__":
    pytest.main()
