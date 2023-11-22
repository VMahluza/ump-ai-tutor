from django.contrib import admin
from .models import *

admin.site.site_url = "/dashboard/"  
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')  # Add the fields you want to display
# Register the User model with the custom admin class
admin.site.register(User, UserAdmin)
admin.site.register(AuthKeys)
admin.site.register(Tutor)
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration)
admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(LoggedTicket)
admin.site.register(Vote)
admin.site.register(Notification)
