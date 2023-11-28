# Create a file, e.g., context_processors.py in your app directory

# context_processors.py

from django.contrib.auth.models import User


def user_count(request):
    user_count = User.objects.count()
    return {'user_count': user_count}
