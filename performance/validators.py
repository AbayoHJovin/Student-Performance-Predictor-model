"""
Validators for the performance prediction model.
This module now uses the StudentPerformance model's validation logic.
"""
from django.core.exceptions import ValidationError
from .models import StudentPerformance

def validate_input_data(data):
    """
    Validate input data for the performance prediction model using the model's validation.
    
    Args:
        data (dict): Dictionary containing input features
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Explicit check for extracurricular range/type as BooleanField can be too lenient
        ext = data.get('extracurricular')
        if not isinstance(ext, (int, bool)) and ext is not None:
             # Try to parse if it's a string, if not raise
             if isinstance(ext, str):
                 if ext.lower() not in ['true', 'false', '0', '1', 'yes', 'no']:
                     return False, ["extracurricular: Must be a boolean value (0, 1, True, False, Yes, No)"]
             else:
                 return False, ["extracurricular: Invalid type"]
        elif isinstance(ext, int) and ext not in [0, 1]:
            return False, ["extracurricular: If provided as integer, must be 0 or 1"]

        # Create a model instance (without saving to DB)
        instance = StudentPerformance(
            hours_studied=data.get('hours_studied'),
            previous_scores=data.get('previous_scores'),
            extracurricular=bool(data.get('extracurricular')) if ext is not None else None,
            sleep_hours=data.get('sleep_hours'),
            sample_papers=data.get('sample_papers')
        )
        
        # Trigger model validation
        instance.full_clean()
        return True, None
        
    except ValidationError as e:
        # Format errors nicely
        errors = []
        if hasattr(e, 'message_dict'):
            for field, messages in e.message_dict.items():
                for msg in messages:
                    errors.append(f"{field}: {msg}" if field != '__all__' else msg)
        else:
            errors = e.messages
            
        return False, errors
    except Exception as e:
        return False, [str(e)]


def preprocess_input_data(data):
    """
    Preprocess input data for the model.
    """
    processed_data = data.copy()
    
    # Convert extracurricular to int for the ML model
    ext = processed_data.get('extracurricular')
    if isinstance(ext, bool):
        processed_data['extracurricular'] = 1 if ext else 0
    elif isinstance(ext, str):
        processed_data['extracurricular'] = 1 if ext.lower() in ['yes', 'true', '1'] else 0
    else:
        processed_data['extracurricular'] = 1 if ext else 0
    
    return processed_data
