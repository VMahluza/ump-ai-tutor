from django import forms
from django.contrib.auth.forms import AuthenticationForm
from dashboard.models import Student, Lecture, Tutor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from dashboard.models import User, AuthKeys, Registration
from django.shortcuts import render, redirect
from .models import UserRequest
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
class LoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

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




class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Email"})
        )    
    username = forms.CharField(
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    first_name = forms.CharField(
        required=True, 
        label="First Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        required=True, 
        label="Last Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    password1 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )

    password2 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    )
    
    # required_css_class = 'form-outline mb-4'
    class Meta:
        model = Student
        fields = [
            'email',
            'username',
            'profile_pic',
            'first_name',
            'last_name',
            'gender',
            'password1',
            'password2'
        ]

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])   
        user.save()
        if commit:   
            user.save()
        return user
    
class TutorSignUpForm(UserCreationForm):
    auth_key = forms.CharField(
        label="Email", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Auth Key" , "disabled": False,  "style": "display: none"})
        )
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Email"})
        )
    
    username = forms.CharField(
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    first_name = forms.CharField(
        required=True, 
        label="First Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        required=True, 
        label="Last Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    password1 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )

    password2 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    )
    
    # required_css_class = 'form-outline mb-4'
    class Meta:
        model = Tutor
        fields = [
            'auth_key',
            'email',
            'username',
            'first_name',
            'last_name',
            'gender',
            'password1',
            'password2'
        ]

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        authkey = AuthKeys.objects.get(authkey=self.instance.auth_key)
        authkey.available = False
        authkey.save()
        user.role = "TUTOR"
        if commit:
            user.save()
        return user

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['course', 'documents', 'level_of_study']
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
        
class UserRequestForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = '__all__'
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
        

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Email"})
        )

    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", "placeholder":"Enter new password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", "placeholder":"Repeat password"}),
    )

class LectureSignUpForm(UserCreationForm):
    auth_key = forms.CharField(
        label="Email", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder":"Auth Key" , "disabled": False, "style": "display: none"})
        )
    email = forms.EmailField(
        required=True, 
        label="Email", 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder":"Email"})
        )
    
    username = forms.CharField(
        required=True, 
        label="Username", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    first_name = forms.CharField(
        required=True, 
        label="First Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        required=True, 
        label="Last Name",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    password1 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your password"})
    )

    password2 = forms.CharField(
        required=True, 
        label="Password",  
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Confirm your password"})
    )
    
    # required_css_class = 'form-outline mb-4'
    class Meta:
        model = Lecture
        fields = [
            'auth_key',
            'email',
            'username',
            'first_name',
            'last_name',
            'gender',
            'password1',
            'password2'
        ]

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        authkey = None
        try:
            authkey = AuthKeys.objects.get(authkey=self.instance.auth_key)
            authkey.available = False
            authkey.save()
            user.role = authkey.role
        except:
            return redirect("/auth/signup/usertype")
          
        finally:
            if commit:
                user.save()
            return user

