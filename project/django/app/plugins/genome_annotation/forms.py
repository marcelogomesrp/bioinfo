# coding: utf-8
from django import forms
from fields import ProjectChoiceField
from models import Annotation, Author, Question, PluginEnrollment, UserFile, Institution, Project


class AnnotationForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Annotation.STATUS_CHOICES, widget=forms.widgets.RadioSelect())
    
    class Meta:
        model = Annotation
        exclude = ('enrollment', 'contig', 'date_added',)
        

class PluginEnrollmentForm(forms.ModelForm):
    def __init__(self, course_class, *args, **kwargs):
        ret = super(PluginEnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['project'].course_class = course_class
        return ret
    
    project = ProjectChoiceField(queryset=Project.objects.all(), widget=forms.RadioSelect,  empty_label=None)
    
    class Meta:
        model = PluginEnrollment
        exclude = ('enrollment', 'date_added', 'tissue')


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('course', 'project', 'date_added')
        

class AddUserFile(forms.ModelForm):
    class Meta:
        model = UserFile
        exclude = ('answer', 'date_added')
    
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.name.split('.')[-1] in ('pdf', 'jpg', 'jpeg', 'zip', 'png', 'gif', 'jpeg'):
            return file
        raise forms.ValidationError('File not supported')


class SubmissionTitleForm(forms.Form):
    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        return super(SubmissionTitleForm, self).__init__(*args, **kwargs)
        
    title = forms.CharField(required=True)
    
    def save(self):
        self.instance.title = self.cleaned_data.get('title')
        self.instance.save()


class AddInstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ('submission',)


class EditInstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ('submission',)
        
        
class AddAuthorForm(forms.ModelForm):
    def __init__(self, submission, *args, **kwargs):
        ret = super(AddAuthorForm, self).__init__(*args, **kwargs)
        self.fields['institution'].queryset = submission.institution_set.all() 
    
    class Meta:
        model = Author
        exclude = ('submission',)


class EditAuthorForm(AddAuthorForm):
    pass