from django.views.generic import TemplateView, View
from .models import AuthKeys
from django.shortcuts import redirect
import uuid
import subprocess
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Student, Lecture, Tutor, Vote
import datetime
from django.core.mail import send_mail



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
        context['top_queries'] = None
        context['current_time'] = str(datetime.datetime.now())
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
        room_name =   f'{self.request.user.id}_{self.request.user.username}'
        course = registration.course
        context['questries'] = Query.objects.filter(course=course)
        context['room_name'] = room_name
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
    user = request.user
    query_id = request.GET.get('q')
    query = Query.objects.get(id=query_id)
    votes_made_by_user_for_query = Vote.objects.filter(user=user, query=query, vote_type=Vote.UPVOTE)

    print("Votes for Query", votes_made_by_user_for_query)
    if not votes_made_by_user_for_query:
        vote = Vote.objects.create(user=user, query=query)
        vote.save()

    return redirect('/dashboard/forum')

def down_vote_query(request):
    user = request.user
    query_id = request.GET.get('q')
    query = get_object_or_404(Query, id=query_id)

    # Check if the user has already voted for this query
    existing_vote = Vote.objects.filter(user=user, query=query, vote_type=Vote.UPVOTE).first()

    print("Down Vote", existing_vote)

    if existing_vote:
     
        # Update the existing vote to be a downvote
        existing_vote.vote_type = Vote.DOWNVOTE
        existing_vote.save()

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
            user.is_online = False
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

from django.views.generic import ListView
from .models import LoggedTicket
class LoggedTicketListView(ListView):
    model = LoggedTicket
    template_name = 'pages/tickets/index.html'
    context_object_name = 'tickets'
    ordering = ['resolve']

def resolveTicket(request):

    ticket_id = request.GET.get('tid')

    try:
        ticket = LoggedTicket.objects.get(id=ticket_id)
        ticket.resolve = True
        ticket.save()

        if ticket.resolve:
            from_email = 'binarybendits@gmail.com'
            recipient_list = [ticket.email]
            subject = f'Ticket #{ticket.id}:  Resolved 😊'
            message = f"""
                Dear {ticket.guest_name},

                We are pleased to inform you that your ticket with reference number #{ticket.id} and subject "{ticket.subject}" has been resolved.

                Our team has thoroughly addressed your concern, and we are happy to assist you further if needed. 
                Feel free to visit the following link for any updates or if you have any additional questions:

                Website: https://ump-ai-tutor-68e7ae10f930.herokuapp.com/

                Thank you for choosing BinaryBendits for your support needs. We appreciate your patience and understanding throughout the process.

                Best regards,

                The BinaryBendits Team
                """

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except:
        return redirect('tickets')

    return redirect('tickets')

