from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np
from .validators import validate_input_data, preprocess_input_data

model = joblib.load('performance/model.pkl')

@api_view(['POST'])
def predict_performance(request):
    data = request.data
    
    # Validate input data
    is_valid, errors = validate_input_data(data)
    if not is_valid:
        return Response({'error': 'Validation failed', 'details': errors}, status=400)
    
    try:
        # Preprocess the data
        processed_data = preprocess_input_data(data)
        
        # Extract features
        features = [
            processed_data['hours_studied'],
            processed_data['previous_scores'],
            processed_data['extracurricular'],
            processed_data['sleep_hours'],
            processed_data['sample_papers']
        ]
        
        # Make prediction
        features = np.array([features])
        prediction = model.predict(features)[0]
        
        # Return prediction
        return Response({
            'performance_index': round(prediction, 2),
            'input_validated': True
        })
    except Exception as e:
        return Response({'error': str(e)}, status=500)
