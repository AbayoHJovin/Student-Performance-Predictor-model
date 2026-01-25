# Student Performance Prediction

A Django-based web application that predicts student performance based on various factors.

## Features

- Machine learning model to predict student performance
- REST API for predictions
- Data visualization

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## API Endpoints

- `/api/predict/`: Get performance predictions

## Technologies Used

- Django
- Django REST Framework
- Scikit-learn
- Pandas
- NumPy
