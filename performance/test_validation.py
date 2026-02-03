"""
Test script for validating the performance prediction model.
This script tests various edge cases to ensure the validation is working correctly.
"""

import os
import sys
import django
import json

# Set up Django environment
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_ml.settings')
django.setup()

from performance.validators import validate_input_data, preprocess_input_data

def print_validation_result(test_name, data, expected_valid):
    """Print the result of a validation test."""
    is_valid, errors = validate_input_data(data)
    
    print(f"\n=== Test: {test_name} ===")
    print(f"Input: {json.dumps(data, indent=2)}")
    print(f"Expected valid: {expected_valid}")
    print(f"Actual valid: {is_valid}")
    
    if errors:
        print(f"Errors: {errors}")
    
    if is_valid == expected_valid:
        print("PASS")
    else:
        print("FAIL")

def run_tests():
    """Run validation tests with various edge cases."""
    
    # Test 1: Valid data
    print_validation_result(
        "Valid data",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        True
    )
    
    # Test 2: Missing field
    print_validation_result(
        "Missing field",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": 1,
            "sample_papers": 5
        },
        False
    )
    
    # Test 3: Invalid hours_studied (negative)
    print_validation_result(
        "Negative hours_studied",
        {
            "hours_studied": -5,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        False
    )
    
    # Test 4: Invalid hours_studied (too high)
    print_validation_result(
        "Too many hours_studied",
        {
            "hours_studied": 20,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        False
    )
    
    # Test 5: Invalid previous_scores (too high)
    print_validation_result(
        "Invalid previous_scores",
        {
            "hours_studied": 7,
            "previous_scores": 120,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        False
    )
    
    # Test 6: Invalid extracurricular (not 0 or 1)
    print_validation_result(
        "Invalid extracurricular",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": 2,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        False
    )
    
    # Test 7: Boolean extracurricular (should be valid)
    print_validation_result(
        "Boolean extracurricular",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": True,
            "sleep_hours": 8,
            "sample_papers": 5
        },
        True
    )
    
    # Test 8: Valid sleep_hours (more than 12 is now allowed if sum <= 24)
    print_validation_result(
        "More than 12 sleep_hours (now valid if total hours <= 24)",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 15,
            "sample_papers": 5
        },
        True
    )
    
    # Test 9: Invalid sample_papers (above new limit of 30)
    print_validation_result(
        "Too many sample_papers (above 30)",
        {
            "hours_studied": 7,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 35
        },
        False
    )
    
    # Test 10: Unrealistic combination (hours_studied + sleep_hours > 24)
    print_validation_result(
        "Unrealistic hours_studied + sleep_hours",
        {
            "hours_studied": 16,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 10,
            "sample_papers": 5
        },
        False
    )
    
    # Test 11: Unrealistic combination (low study hours but many sample papers)
    print_validation_result(
        "Unrealistic study hours vs sample papers",
        {
            "hours_studied": 0.5,
            "previous_scores": 85,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 10
        },
        False
    )
    
    # Test 12: Edge case (minimum valid values)
    print_validation_result(
        "Minimum valid values",
        {
            "hours_studied": 0,
            "previous_scores": 0,
            "extracurricular": 0,
            "sleep_hours": 0,
            "sample_papers": 0
        },
        True
    )
    
    # Test 13: Edge case (maximum valid values)
    print_validation_result(
        "Maximum valid values",
        {
            "hours_studied": 16,
            "previous_scores": 100,
            "extracurricular": 1,
            "sleep_hours": 8,
            "sample_papers": 20
        },
        True
    )
    
    # Test 14: The example from the user
    print_validation_result(
        "User example (24 hours studied, 24 sleep hours)",
        {
            "hours_studied": 24,
            "previous_scores": 60,
            "extracurricular": 1,
            "sleep_hours": 24,
            "sample_papers": 3
        },
        False
    )

if __name__ == "__main__":
    run_tests()