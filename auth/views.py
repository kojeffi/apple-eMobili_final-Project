from django.shortcuts import render, redirect
from .forms import RegistrationForm, User
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have registered successfully')
            return redirect('registration-url')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {"form": form})



from django.shortcuts import render
from django.contrib.auth.models import User  # Import the User model

# def register(request):
#     # Fetch the list of users from the database
#     users = User.objects.all()
#
#     context = {
#         'users': users,
#     }
#
#     return render(request, 'dashboard/forms-elements.html', context)
