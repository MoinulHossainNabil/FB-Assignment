from django import forms
from django.core.validators import FileExtensionValidator


class ApplicationForm(forms.Form):
    POSITIONS = (
        ('M', 'Mobile'),
        ('B', 'Backend'),
    )
    # tsync_id = forms.UUIDField()
    name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(max_length=14, required=True)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=256, required=True)
    graduation_year = forms.IntegerField(max_value=2020, min_value=2015, required=True)
    cgpa = forms.FloatField(max_value=4.0, min_value=2.0, required=False)
    experience_in_months = forms.IntegerField(max_value=100, min_value=0, required=False)
    current_work_place_name = forms.CharField(max_length=256, required=False)
    applying_in = forms.ChoiceField(choices=POSITIONS, required=True)
    expected_salary = forms.IntegerField(max_value=60000, min_value=15000, required=True)
    field_buzz_reference = forms.CharField(max_length=256, required=False)
    github_project_url = forms.URLField(max_length=512, required=True)
    cv_file = forms.FileField(required=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

