from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(AuthKeys)
admin.site.register(Tutor)
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Registration)
admin.site.register(Query)
admin.site.register(Answer)
