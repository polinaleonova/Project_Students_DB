from django.contrib import admin
from models_project.models import *

class StudentInline(admin.TabularInline):
    model = Student


class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline,]


class StudentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
