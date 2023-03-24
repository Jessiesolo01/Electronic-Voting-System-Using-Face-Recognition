from django.contrib import admin
from .models import StudentData, Position, Candidate
# from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.contrib.auth.models import Group
# from django.utils.translation import gettext_lazy as _


# Register your models here.
# admin.site.unregister(Group)

admin.site.register(StudentData)
# admin.site.register(FaceCapture)
admin.site.register(Position)
admin.site.register(Candidate)
# admin.site.register(Voted)
# admin.site.register(ControlVote)



