from django import forms
from models import Department, Institution

class AddInstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department