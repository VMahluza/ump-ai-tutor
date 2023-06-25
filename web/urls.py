from .views import HomePageView, CustomLoginView,StudentSignUpView, UserTypePageView,RegistrationPageView , TutorSignUpView, LectureSignUpView
from django.urls import path, include, re_path


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/signup/student', StudentSignUpView.as_view(), name='signup-student'),
    path('auth/signup/tutor', TutorSignUpView.as_view(), name='tutor-student'),
    path('auth/signup/tutor/?key=<str:accesskey>', TutorSignUpView.as_view(), name='tutor-student'),
    path('auth/signup/usertype', UserTypePageView.as_view(), name='usertype'),
    re_path(r'^auth/signup/tutor/$', TutorSignUpView.as_view(), name='tutor-signup'),
    re_path(r'^auth/signup/lecture/$', LectureSignUpView.as_view(), name='lecture-signup'),
    path('registration/', RegistrationPageView.as_view(), name='complete-registration'),
    # Other URL patterns...
]
