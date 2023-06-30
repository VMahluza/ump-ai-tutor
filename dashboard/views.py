from django.views.generic import TemplateView, View
from .models import AuthKeys
from django.shortcuts import redirect
import uuid
from .models import Registration, Answer, User
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .forms import  QueryForm, AnswerForm, UserProfileUpdateForm,ChangePasswordForm
from django.views.generic import CreateView
from dashboard.models import AuthKeys, Registration, Query, Module
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Student, Lecture, Tutor
import datetime



# Create your views here.
class HomeDashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard-index.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['registration'] = Registration.objects.get(user=self.request.user)
        context['students_count'] = Student.student.count()
        context['tutors_count'] = Tutor.tutor.count()
        context['lecture_count'] = Lecture.lecture.count()
        context['top_queries'] = Query.objects.order_by('-votes')[:6]
        context['current_time'] = str(datetime.datetime.now())


        # Add more data to the context if needed
        return context
# Create your views here.

# Create your views here.
class ActiveUsersboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/users/index.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        register = Registration.objects.get(user=self.request.user)
        context['title'] = 'Participants'
        context['registration'] = register
        context['active_users'] = Registration.objects.filter(course=register.course)
        # Add more data to the context if needed
        return context
# Create your views here.


class TutorDashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/tutor/index.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tutors'
        context['accesskey'] = AuthKeys.objects.filter(user=self.request.user).last()
        # Add more data to the context if needed
        return context
class UserProfilePageView(LoginRequiredMixin, UpdateView):
    template_name = 'pages/profile/index.html'
    login_url = '/auth/login/'
    # form_class = UserProfileUpdateForm
    success_url = reverse_lazy('profile')
    form_class = UserProfileUpdateForm
    # change_password_form = UserProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        context["password_error"] = self.request.GET.get('password_error')

        context['registration'] = Registration.objects.get(user=self.request.user)
        context['accesskey'] = AuthKeys.objects.filter(user=self.request.user).last()
        # Add more data to the context if needed
        return context
    def get_object(self, queryset=None):
        return self.request.user
    
    


# # Create your views here.
class QAForumPageView(LoginRequiredMixin, CreateView):
    template_name = 'pages/forum/index.html'
    form_class = QueryForm
    success_url = '/dashboard/forum'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'QA Forum'
        # context['answer_form'] = AnswerForm()
        registration = Registration.objects.get(user=self.request.user)
        course = registration.course
        context['questries'] = Query.objects.filter(course=course)

        # Assuming you have an instance of the Query model called `query`
        
        # Add more data to the context if needed
        return context
    
    def form_valid(self, form):
        # Set the user for the query to the current user
        registration = Registration.objects.get(user=self.request.user)
        form.instance.user = self.request.user
        form.instance.course=registration.course
        return super().form_valid(form)
    

    
def generate_auth_key( request):
    rand_auth_key = (str(uuid.uuid4())[:8]).upper()
    if not AuthKeys.objects.filter(authkey=rand_auth_key).exists():
        AuthKeys.objects.create(authkey=rand_auth_key, user=request.user, available=True, role="TUTOR").save()

    return redirect('tutor')

def up_vote_query(request):
    query_id = request.GET.get('q')
    query = Query.objects.get(id=query_id)
    query.votes += 1
    query.save()
    return redirect('/dashboard/forum')
def down_vote_query(request):
    query_id = request.GET.get('q')
    query = Query.objects.get(id=query_id)
    query.votes -= 1
    query.save()
    return redirect('/dashboard/forum')



def add_answer_to_query(request):
    print("From dashboard")
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text') # Retrieve the answer_text from the form data
        query_id = request.POST.get('query_id') # Retrieve the answer_text from the form data
        # Access other form fields in a similar manner
        print(answer_text)
        answer = Answer.objects.create(
            user = request.user,
            answer_text = answer_text,
            query = Query.objects.get(id=int(query_id))
        )
        # Process the form data
        # ...   
        answer.save()

        return redirect('/dashboard/forum?a=new')  # Redirect to the desired URL after processing the form

    # Handle the case when the request method is not POST
    # ...

    return redirect('/dashboard/forum') 

class LogoutView(View):
    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        if user.is_active:
            user.is_active = False
            user.save()

        logout(request)
        # return redirect('/login')
        return redirect('/auth/login/')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To update the user's session
            return redirect('profile')  # Redirect to the profile page or any other desired page after successful password change
    else:
        form = ChangePasswordForm(request.user)
    return redirect('./profile?password_error=wrong_password')



