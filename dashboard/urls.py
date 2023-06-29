from .views import HomeDashboardPageView, change_password, ActiveUsersboardPageView ,UserProfilePageView, QAForumPageView, TutorDashboardPageView, generate_auth_key, up_vote_query, down_vote_query, add_answer_to_query
from django.urls import path, include


urlpatterns = [
    path('', HomeDashboardPageView.as_view(), name='home'),
    path('', HomeDashboardPageView.as_view(), name='dashboard'),
    path('forum', QAForumPageView.as_view(), name='forum'),
    path('forum/query/up', up_vote_query, name='upvote-query'),
    path('forum/query/down', down_vote_query, name='downvote-query'),
    path('active-users', ActiveUsersboardPageView.as_view(), name='active-users'),
    path('tutor', TutorDashboardPageView.as_view(), name='tutor'),
    path('generate-auth-key', generate_auth_key, name='generate-auth-key'),
    path('add-answer-to-query', add_answer_to_query, name='add-answer-to-query'),
    path('profile', UserProfilePageView.as_view(), name='profile'),
    path(r'^profile/$', UserProfilePageView.as_view(), name='profile-param'),
    path('change-password', change_password, name='change-password'),
    # Other URL patterns...
]