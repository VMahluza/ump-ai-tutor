from django.shortcuts import render
from django.views.generic import TemplateView
from .models import AuthKeys
from django.shortcuts import redirect
import uuid
from .models import Registration

# Create your views here.
class HomeDashboardPageView(TemplateView):
    template_name = 'dashboard-index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['registration'] = Registration.objects.get(user=self.request.user)

        # Add more data to the context if needed
        return context
# Create your views here.
class TutorDashboardPageView(TemplateView):
    template_name = 'pages/tutor/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tutors'
        context['accesskey'] = AuthKeys.objects.filter(user=self.request.user).last()
        # Add more data to the context if needed
        return context
    


    
# Create your views here.
class QAForumPageView(TemplateView):
    template_name = 'pages/forum/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'QA Forum'
        # Add more data to the context if needed
        return context
    
def generate_auth_key( request):
    rand_auth_key = (str(uuid.uuid4())[:8]).upper()
    if not AuthKeys.objects.filter(authkey=rand_auth_key).exists():
        AuthKeys.objects.create(authkey=rand_auth_key, user=request.user, available=True, role="TUTOR").save()

    return redirect('tutor')
