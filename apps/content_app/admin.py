from django.contrib import admin
from .models import User
from ..content_app.models import Appt

admin.site.register(User)
admin.site.register(Appt)

