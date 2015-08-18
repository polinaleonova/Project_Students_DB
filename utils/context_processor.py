from django.conf import settings


def my_settings(request):
    return {
        'settings': settings
    }