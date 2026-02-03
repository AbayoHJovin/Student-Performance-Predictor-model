from django.db import models
from django.core.exceptions import ValidationError

def validate_hours_studied(value):
    if value < 0 or value > 24:
        raise ValidationError("Hours studied must be between 0 and 24.")

def validate_previous_scores(value):
    if value < 0 or value > 100:
        raise ValidationError("Previous scores must be between 0 and 100.")

def validate_sleep_hours(value):
    if value < 0 or value > 24:
        raise ValidationError("Sleep hours must be between 0 and 24.")

def validate_sample_papers(value):
    if value < 0 or value > 30:
        raise ValidationError("Sample papers must be between 0 and 30.")

class StudentPerformance(models.Model):
    hours_studied = models.FloatField(validators=[validate_hours_studied])
    previous_scores = models.IntegerField(validators=[validate_previous_scores])
    extracurricular = models.BooleanField()
    sleep_hours = models.FloatField(validators=[validate_sleep_hours])
    sample_papers = models.IntegerField(validators=[validate_sample_papers])
    performance_index = models.FloatField(null=True, blank=True)

    def clean(self):
        super().clean()
        
        errors = {}
        
        # 1. Total hours in a day cannot exceed 24
        if self.hours_studied is not None and self.sleep_hours is not None:
            total_time = self.hours_studied + self.sleep_hours
            if total_time > 24:
                errors['__all__'] = f"Impossible schedule: Study hours ({self.hours_studied}) and sleep hours ({self.sleep_hours}) combined ({total_time}h) exceed a 24-hour day."
        
        # 2. Minimum sleep for long-term study (Optional/Warning, but here as a hard limit for "reality")
        # The user said 2 hours should validate, so we allow it.
        
        # 3. Sample papers vs study hours reality check
        if self.hours_studied is not None and self.sample_papers is not None:
             # If someone studies less than 1 hour, they probably can't do more than 5 sample papers.
             if self.hours_studied < 1.0 and self.sample_papers > 5:
                errors['sample_papers'] = "Unrealistic number of sample papers for the amount of study time."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"Performance Index: {self.performance_index}"
