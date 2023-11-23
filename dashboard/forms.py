from django import forms
from .models import Query, Answer, User, LoggedTicket, Registration, LearningMaterial
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import PasswordChangeForm


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['module', 'question_text', ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                
                "class": 'form-control',
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
class LearningMaterialForm(forms.ModelForm):
    class Meta:
        model = LearningMaterial
        fields = ['file', 'name', 'is_public']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                
                "class": 'form-control',
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                
                "class": 'form-control',
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_pic', 'gender']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = { 
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
class LearningMaterialUpdateForm(forms.ModelForm):
    class Meta:
        model = LearningMaterial
        fields = ['file', 'name', 'is_public']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = { 
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class RegistrationUpdateForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['documents']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = { 
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )


class LoggedTicketForm(forms.ModelForm):
    class Meta:
        model = LoggedTicket
        fields = ['guest_name', 'email', 'subject', 'message']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = { 
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = { 
                "class": 'form-control'
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )