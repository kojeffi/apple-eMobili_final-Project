from django.shortcuts import render, redirect
from django.contrib import messages

from dashbord.models import RecognizedAlphabet
from dashbord.views import word_label
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout


def admin(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard/index.html', {'username': request.user.username})
    return render(request, 'dashboard/index.html')


def register_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']  # Add this line to get email from the form

        if not CustomUser.objects.filter(username=username).exists():
            # Provide the email parameter when creating the user
            user = CustomUser.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('register_admin-url')
        else:
            messages.error(request, 'User already registered.')

    return render(request, 'dashboard/pages-register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f'User {user.username} is_staff: {user.is_staff}')  # Add this line
            if user.is_staff:
                return redirect('admin-url')
            else:
                return redirect('dashbord-url')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'dashboard/pages-login.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:  # Check if the user is an admin
                return redirect('admin-url')  # Redirect admin to admin page
            else:
                return redirect('dashbord-url')  # Redirect regular user to user dashboard
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'dashboard/pages-login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('home-url')


# auth/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from .models import User

# admin_app/views.py

from django.shortcuts import render

# admin_app/views.py

# admin_app/views.py

from django.contrib.auth.models import User  # Import Django's User model


def forms_elements(request):
    users = User.objects.all()  # Query all users

    context = {
        'users': users,
    }

    return render(request, 'dashboard/forms-elements.html', context)


from django.shortcuts import render
from .models import User  # Import your User model


def update_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user_username = request.POST.get('username')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        user.username = user_username
        user.email = user_email
        user.password = user_password
        user.save()
        messages.success(request, 'User updated successfully')
        return redirect('forms_elements-url')
    return render(request, 'dashboard/forms-layouts.html', {'user': user})


# def update_user(request, id):
#     user = get_object_or_404(User, id=id)
#
#     if request.method == "POST":
#         form = RegistrationForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'User updated successfully')
#             return redirect('user_table-url')
#     else:
#         form = RegistrationForm(instance=user)
#
#     return render(request, 'dashboard/forms-layouts.html', {'form': form})
#

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('forms_elements-url')


# def delete_user(request, id):
#     user = get_object_or_404(User, id=id)
#
#     if request.method == "POST":
#         user.delete()
#         messages.success(request, 'User deleted successfully')
#         return redirect('forms_elements-url')
#
#     return render(request, 'dashboard/forms-elements.html', {'user': user})


from django.shortcuts import render
from django.contrib.auth.models import User  # Import the User model


def register(request, id):
    # Fetch the list of users from the database
    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'dashboard/forms-elements.html', context)


# In views.py
from django.shortcuts import render


def tables_general(request, id):
    recognized_alphabets = RecognizedAlphabet.objects.all()
    return render(request, 'dashboard/tables-general.html', {'recognized_alphabets': recognized_alphabets})


#
# def table(request, id):
#     # Retrieve recognized alphabets from the database
#     recognized_alphabets = RecognizedAlphabet.objects.all()
#     return render(request, 'dashboard/tables-general.html', {'recognized_alphabets': recognized_alphabets})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login_admin-url')
# def dashboard(request):
#     # You can add logic here if needed
#     return render(request, 'dashboard/dashboard.html')

@login_required(login_url='login_admin-url')
def tables_general(request, id):
    # You can add logic here if needed
    recognized_alphabets = RecognizedAlphabet.objects.all()
    return render(request, 'dashboard/tables-general.html', {'recognized_alphabets': recognized_alphabets})


def save_recognized_alphabets(request, id):
    global word, running, word_label

    if request.method == 'POST':
        # Get the recognized alphabets
        recognized_word = " ".join(word)

        # Save the recognized word as a single entry in the database
        recognized_alphabet = RecognizedAlphabet.objects.create(alphabet=recognized_word)

        # Retrieve all recognized alphabets from the database
        recognized_alphabets = RecognizedAlphabet.objects.all()

        # Display the recognized alphabets immediately after saving
        return render(request, 'dashbord/dashbord.html',
                      {'recognized_alphabets': recognized_alphabets,
                       'running': running,
                       'start_button_text': "Start Process",
                       'word_label': word_label})

    return render(request, 'dashboard/tables-general.html',
                  {'running': running, 'start_button_text': "Start Process", 'word_label': word_label})


from django.shortcuts import render, redirect
from .models import ContactMessage

# views.py

from django.shortcuts import render, redirect
from .models import ContactMessage

# def contact(request):
#     sent_message = None
#
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#
#         ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
#
#         sent_message = 'Your message has been sent. Thank you!'
#
#     return render(request, 'dashboard/pages-contact.html', {'sent_message': sent_message})
#

from django.shortcuts import render, redirect
from .models import ContactMessage


def contact(request):
    if request.method == 'POST':
        # Process form submission and save to database
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message_body = request.POST['message']

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_body
        )

        return redirect('contact-url')  # Redirect to the same page after submission

    # Retrieve messages from the database
    messages = ContactMessage.objects.all()

    return render(request, 'dashboard/pages-contact.html', {'messages': messages})
