from .views import HomeDashboardPageView, QAForumPageView, TutorDashboardPageView, generate_auth_key
from django.urls import path, include


urlpatterns = [
    path('', HomeDashboardPageView.as_view(), name='home'),
    path('', HomeDashboardPageView.as_view(), name='dashboard'),
    path('forum', QAForumPageView.as_view(), name='forum'),
    path('tutor', TutorDashboardPageView.as_view(), name='tutor'),
    path('generate-auth-key', generate_auth_key, name='generate-auth-key'),
    # Other URL patterns...
]