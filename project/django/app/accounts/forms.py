# coding: utf-8
from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.localflavor.br.forms import BRStateSelect
from django.contrib.formtools.wizard import FormWizard
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from models import UserProfile


class UserProfileForm(forms.ModelForm):
    name = forms.RegexField(label=_('Full name'), regex=r'^.+\s+.+$')
    email = forms.EmailField(label=_('E-mail'))
    enrollment_year = forms.RegexField(label=_('Enrollment year'), regex=r'^\d{4}$')
    institution_state = forms.CharField(label=_('State'), widget=BRStateSelect())
    birth_date = forms.DateField(label=_('Birth date'), input_formats=['%d/%m/%Y'])

    class Meta:
        model = UserProfile
        exclude = ('user', 'registration_date', 'last_update')
        fields = ['name', 'email', 'birth_date', 'institution_name', 'institution_city',
                    'institution_state', 'course', 'enrollment_year',]

    def save(self, commit, *args, **kwargs):
        obj = super(UserProfileForm, self).save(commit=commit)
        if not commit:
            obj.name = self.cleaned_data['name']
            obj.email = self.cleaned_data['email']
        return obj

    def clean_enrollment_year(self):
        value = int(self.cleaned_data['enrollment_year'])
        if value > datetime.now().year or value < 1900:
            raise forms.ValidationError(_('Please enter a valid year'))
        return value


class UserLoginForm(UserCreationForm):
    def get_template(self, step):
        return ['accounts/wizard_%s.html' % step, 'accounts/wizard.html']


class RegistrationWizard(FormWizard):
    def done(self, request, form_list):
        profile, user = [form.save(commit=False) for form in form_list]
        user.first_name, user.last_name = profile.name.split(' ', 1)
        user.email = profile.email
        user.save()
        profile.user = user
        profile.save()        
        u = authenticate(username=user.username, password=request.POST.get('1-password1'))
        auth_login(request, u)

        messages.info(request, _('Registration completed. Please select a institution  bellow to get enrolled in a class.'))
        return redirect('list_institutions')

    def get_template(self, step):
        return ['accounts/wizard_%s.html' % step, 'accounts/wizard.html']
