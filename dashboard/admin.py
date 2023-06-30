from django.contrib import admin
from .models import *

from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _

# Define a custom AdminConfig class
class MyAdminConfig(AdminSite):
    site_title = _('AI Tutor Admin')  # Set the admin site title
    site_header = _('AI Tutor Admin')  # Set the text displayed as the admin site header
    index_title = _('Welcome to Admin')  # Set the text displayed on the admin site index page
# Create an instance of the custom AdminConfig class
my_admin_site = MyAdminConfig(name='myadmin')

# Register your models with the custom admin site
my_admin_site.register(User)
my_admin_site.register(AuthKeys)
my_admin_site.register(Tutor)
my_admin_site.register(Lecture)
my_admin_site.register(Student)
my_admin_site.register(Course)
my_admin_site.register(Module)
my_admin_site.register(Registration)
my_admin_site.register(Query)
my_admin_site.register(Answer)

