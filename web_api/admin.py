from django.contrib import admin
from .models import User, Place, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Place)
admin.site.register(Message)
