from django.contrib import admin
from models_project.models import *


class StudentInline(admin.TabularInline):
    model = Student


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name_group', 'monitor']
    inlines = [StudentInline]


class StudentAdmin(admin.ModelAdmin):
    pass
    list_display = ['student_name', 'date_birthday', 'ticket_number', 'get_thumbnail_html']


admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(History)