import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_ml.settings')
django.setup()

import pandas as pd
from performance.models import StudentPerformance

df = pd.read_csv('performance/dataset.csv')

objects = []
for index, row in df.iterrows():
    extracurricular = row['Extracurricular Activities'] == 'Yes'
    objects.append(StudentPerformance(
        hours_studied=row['Hours Studied'],
        previous_scores=row['Previous Scores'],
        extracurricular=extracurricular,
        sleep_hours=row['Sleep Hours'],
        sample_papers=row['Sample Question Papers Practiced'],
        performance_index=row['Performance Index']
    ))

StudentPerformance.objects.bulk_create(objects)