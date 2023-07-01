from .views import HomePageView, CustomLoginView,StudentSignUpView, UserTypePageView,RegistrationPageView , TutorSignUpView, LectureSignUpView
from django.urls import path, include, re_path
from .views import CustomPasswordResetView, CustomPasswordResetCompleteView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, contactUs
from django.contrib.auth import views as auth_views

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
  # Other URL patterns
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact-us/', contactUs, name='contact-us'),
    # Other URL patterns

]
