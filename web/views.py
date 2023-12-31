from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, FormView
from .manip import *
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistrationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .forms import StudentSignUpForm, TutorSignUpForm, LectureSignUpForm, UserRequestForm, CustomPasswordResetForm, CustomSetPasswordForm
from dashboard.models import AuthKeys, Registration
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from dashboard.models import Query
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from dashboard.models import User, LoggedTicket

from django.contrib.auth.views import PasswordResetView
class HomePageView(CreateView):
    template_name = 'index.html'
    form_class = UserRequestForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Welcome to the home page!'   
        feature_items = [
            FeatureItemData(
                title="Intelligent Chatbot", 
                description="The AI Tutoring System incorporates an intelligent chatbot that provides personalized support to students. It uses natural language processing and machine learning algorithms to understand and respond to student queries effectively.",
                icon_div=IconDiv(
                    icon_class="bi bi-briefcase",
                    color="#f57813",
                    delay=100)
                ),
            FeatureItemData(
                title="Question Asking Forum", 
                description="The app features a question asking forum where students can post their questions and receive answers from peers and educators. This fosters collaboration, knowledge sharing, and a sense of community among learners.",
                icon_div=IconDiv(
                    icon_class="bi bi-briefcase",
                    color="#15a04a",
                    delay=200)
                ),
            FeatureItemData(
                title="Personalized Learning Path", 
                description="Students can interact with each other without distractions from other barriers",
                icon_div=IconDiv(
                    icon_class="bi bi-bar-chart",
                    color="#d90769",
                    delay=300)
                ),
        ]

        context['feature_items'] = feature_items
        context['top_queries'] = None
        # Add more data to the context if needed
        return context
    
class UserTypePageView(TemplateView):
    template_name = 'auth/user-type.html'
    access_key_error_message = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Welcome to the home page!'
        context['accesskey_denied'] = self.access_key_error_message
        # Add more data to the context if needed
        return context
    
    def post(self, request,*args, **kwargs):
        access_key = request.POST.get('access_key')
        if access_key == None or access_key == '':
            return redirect('/auth/signup/student')
        
        authkey = None

        try:
            authkey = AuthKeys.objects.get(authkey=access_key)
        except:
          return redirect('/auth/signup/usertype')

        if authkey is None:
            self.access_key_error_message = "This access key does not exist"
            return redirect('/auth/signup/usertype')
            

        if authkey.available == False:
            self.access_key_error_message = "This access key was used before"
            return redirect('/auth/signup/usertype')


        if authkey.available and authkey.role == 'TUTOR':
            return redirect(f'/auth/signup/tutor/?key={access_key}')
        
        if authkey.available and authkey.role == 'LECTURE':
            
            return redirect(f'/auth/signup/lecture/?key={access_key}')
            
        
        return redirect("/")

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    def get_success_url(self):
        user = User.objects.get(id=self.request.user.id)
        if not user.is_online:
            user.is_online = True
            user.save()
            
        registration = Registration.objects.filter(user=self.request.user)
        if registration:
            return reverse_lazy('dashboard')
        else:
            return reverse_lazy('complete-registration')
        
class RegistrationPageView(CreateView):
    template_name = 'registration/index.html'
    form_class = RegistrationForm
    success_url = '/dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        # Save the form and associate it with the current user
        registration = form.save(commit=False)
        registration.user = self.request.user
        registration.save()
        return super().form_valid(form)



class StudentSignUpView(CreateView):
    template_name = 'auth/signup.html'
    form_class = StudentSignUpForm
    success_url = '/auth/login'
    login_url = '/auth/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Student"
        return context


class TutorSignUpView(UserPassesTestMixin, CreateView):
    template_name = 'auth/signup.html'

    form_class = TutorSignUpForm
    success_url = '/auth/login'
    login_url = reverse_lazy('usertype') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Tutor"
        return context


    def test_func(self):
        accesskey = self.request.GET.get('key').strip()

        number_of_accesskeys = AuthKeys.objects.filter(authkey=accesskey, available=True).count()

        if number_of_accesskeys > 0:
            return True
        else:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Lecture"

        accesskey = self.request.GET.get('key')
        context['accesskey'] = accesskey
        context['accesskey_hidden'] = accesskey[:2] + "*" * 5 +  accesskey[7:]
        return context
class LectureSignUpView(UserPassesTestMixin, CreateView):
    template_name = 'auth/signup.html'
    form_class = LectureSignUpForm
    success_url = '/auth/login'
    login_url = '/auth/login'
    

    def test_func(self):

        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Lecture"
        accesskey = self.request.GET.get('key')
        context['accesskey'] = accesskey
        context['accesskey_hidden'] = accesskey[:4] + "*" * 5 +  accesskey[7:]

        print("\n\n\n\n" * 2,accesskey[3], "\n\n\n\n" * 2)

        # Add more data to the context if needed
        return context

    # views.py

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    # from_email = "binarybendits@gmail.com"
    email_template_name = 'auth/password_reset_email.html'
    success_url = '/auth/login'

    def form_valid(self, form): 
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = "auth/password_reset_confirm.html"
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"


def contactUs(request):
    if request.method == "POST":
        guest_name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(guest_name, email, subject, message)

        try:
            logged = LoggedTicket.objects.create(
                guest_name=guest_name,
                email=email,
                subject=subject,
                message=message
            )

            print(logged)

            logged.save()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return redirect('/')
        
        return redirect('/')
    else:
        return redirect('/')

    

