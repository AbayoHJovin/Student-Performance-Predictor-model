from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import numpy as np

model = joblib.load('performance/model.pkl')

@api_view(['POST'])
def predict_performance(request):
    data = request.data
    try:
        features = [
            data['hours_studied'],
            data['previous_scores'],
            data['extracurricular'],
            data['sleep_hours'],
            data['sample_papers']
        ]
        features = np.array([features])
        prediction = model.predict(features)[0]
        return Response({'performance_index': round(prediction, 2)})
    except KeyError:
        return Response({'error': 'Missing required fields'}, status=400)
