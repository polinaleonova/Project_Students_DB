import json

from django.core.management.base import BaseCommand
from models_project import models


class Command(BaseCommand):
    help = 'Commands for project'

    def show_groups(self, *args, **options):
        """
        command for run:
        python manage.py commands show_groups
        """
        return json.dumps([{
            'group name': group.name_group,
            'praepostor': str(group.praepostor),
            'students': [
                {
                    'name': student.student_name,
                    'date of birthday': str(student.date_birthday),
                    'ticket number': student.ticket_number
                } for student in group.student_set.all()]
        } for group in models.Group.objects.all()])

    def handle(self, *args, **options):
        action = args[0]
        if hasattr(self, action):
            return getattr(self, action)(*args[1:], **options)
