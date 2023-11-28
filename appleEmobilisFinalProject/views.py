from django.shortcuts import render

from admin_app.models import ContactMessage


def home(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard/index.html')


def contact(request):
    sent_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        sent_message = 'Your message has been sent. Thank you!'

    return render(request, 'pages-contact.html', {'sent_message': sent_message})
