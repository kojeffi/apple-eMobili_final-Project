from django.shortcuts import render, redirect
from django.contrib import messages
import cv2
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import mediapipe as mp
import numpy as np
import math
import time
from threading import Thread
import pyttsx3
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import json
from .credentials import *

# Initialize the webcam capture
cap = cv2.VideoCapture(0)

# Initialize the hand detector and classifier
detector = HandDetector(maxHands=1)
classifier = Classifier("dashbord/keras_model.h5", "dashbord/labels.txt")

offset = 20
imgSize = 300

labels = ["1","2","3","4","5","6","7","8","9","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
          "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

word = []
word_label = ""

# Function to start/stop the hand tracking and classification process

running = False


def toggle_process(request):
    global running, word_label
    running = not running
    if running:
        start_button_text = "Stop Process"
        # Update this line to match your HTML button element
        process_thread = Thread(target=process)
        process_thread.start()
    else:
        start_button_text = "Start Process"  # Update this line to match your HTML button element
    return render(request, 'dashbord/dashbord.html',
                  {'running': running, 'start_button_text': start_button_text, 'word_label': word_label})


# Function to handle hand tracking and classification process
def process():
    global running, word, word_label
    while running:
        success, img = cap.read()
        if not success:
            continue

        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)

            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                alphabet = labels[index]
                word.append(alphabet)
                speak_alphabet(alphabet)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                alphabet = labels[index]
                word.append(alphabet)
                speak_alphabet(alphabet)

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90,
                                                                     y - offset - 50 + 50), (255, 0, 255),
                          cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 28), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

        cv2.imshow("Image", imgOutput)
        if cv2.waitKey(1) == ord('q'):
            break

        word_label = "Recognized Alphabets: " + " " + " ,".join(word)
    cv2.destroyAllWindows()


# Function to convert alphabet to speech
def speak_alphabet(alphabet):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(alphabet)
    engine.runAndWait()


# Function to clear the recognized word
def clear_word(request):
    global word, word_label
    word = []
    word_label = "Recognized Alphabets:"
    return render(request, 'dashbord/dashbord.html',
                  {'running': running, 'start_button_text': "Start Process", 'word_label': word_label})


#
#
from django.shortcuts import render, redirect


#
#


#

# from django.contrib.auth.views import login

# Function to stream video frames and recognized words to the front end
def video_feed(request):
    def generate_frames():
        global word_label
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            # Yield the recognized words as a Server-Sent Event (SSE)
            yield "data: {0}\n\n".format(word_label)

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


import os

# views.py

from .models import RecognizedAlphabet

# views.py

from django.shortcuts import render, redirect
from .models import RecognizedAlphabet  # Import the RecognizedAlphabet model

# views.py
from .models import RecognizedAlphabet

from django.shortcuts import render, redirect
from .models import RecognizedAlphabet

from django.shortcuts import render, redirect
from .models import RecognizedAlphabet


def save_recognized_alphabets(request):
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

    return render(request, 'dashbord/dashbord.html',
                  {'running': running, 'start_button_text': "Start Process", 'word_label': word_label})


# views.py
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import RecognizedAlphabet

# views.py

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import RecognizedAlphabet
# views.py

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import RecognizedAlphabet


def download_table_as_pdf(request):
    # Retrieve the latest 10 recognized alphabets from the database
    recognized_alphabets = RecognizedAlphabet.objects.order_by('-id')[:10]

    # Extract the alphabet values from the queryset
    alphabets = [alphabet.alphabet for alphabet in recognized_alphabets]

    # Combine the alphabet values into a single string separated by commas
    alphabets_str = ', '.join(alphabets)

    # Create the response object with appropriate headers for PDF download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recognized_alphabets.pdf"'

    # Create a PDF document
    pdf = canvas.Canvas(response)

    # Set up the PDF document layout
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, 'Recognized Gestures')

    # Write data row with alphabets separated by commas
    pdf.drawString(100, 780, alphabets_str)

    # Close the PDF document
    pdf.save()

    return response


from django.shortcuts import render
from .models import RecognizedAlphabet


def dashbord(request):
    # Retrieve recognized alphabets from the database
    recognized_alphabets = RecognizedAlphabet.objects.all()

    return render(request, 'dashbord/dashbord.html', {'recognized_alphabets': recognized_alphabets, 'running': running,
                                                      'start_button_text': "Start Process", 'word_label': word_label})


from django.shortcuts import render, redirect, get_object_or_404
from .models import RecognizedAlphabet

# views.py

from django.shortcuts import redirect

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import RecognizedAlphabet


def delete(request, id):
    alphabet = get_object_or_404(RecognizedAlphabet, id=id)
    alphabet.delete()
    messages.success(request, 'Alphabet deleted successfully.')
    return redirect('dashbord-url')


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Import any other necessary modules

def clear_recognized_alphabets(request):
    # Logic to clear the recognized alphabets goes here
    # For example, you can clear the 'recognized_alphabets.txt' file
    file_path = "recognized_alphabets.txt"

    # Ensure the file exists and open it in write mode to clear its contents
    if os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")

    # Redirect back to the 'view_recognized_alphabets' view
    return HttpResponseRedirect(reverse('view_recognized_alphabets'))


from django.shortcuts import render
from django.http import HttpResponse
from .models import RecognizedAlphabet
import requests

# Import statements
import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
from django.http import HttpResponse
from django.shortcuts import render
from .models import RecognizedAlphabet  # Assuming your model is in a file named models.py

# Your class definitions here...
from django.shortcuts import render
from django.http import HttpResponse
from .models import RecognizedAlphabet
import requests


from django.shortcuts import render, redirect, get_object_or_404
from .models import RecognizedAlphabet
from .forms import RecognizedAlphabetForm
import requests
from django.http import HttpResponse

# Existing code...

def save_recognized_alphabets(request):
    global word, running, word_label

    if request.method == 'POST':
        form = RecognizedAlphabetForm(request.POST, request.FILES)

        if form.is_valid():
            recognized_word = " ".join(word)
            form.save(commit=False)
            form.instance.alphabet = recognized_word
            form.save()

            recognized_alphabets = RecognizedAlphabet.objects.all()

            return render(request, 'dashbord/dashbord.html',
                          {'recognized_alphabets': recognized_alphabets,
                           'running': running,
                           'start_button_text': "Start Process",
                           'word_label': word_label})

    else:
        form = RecognizedAlphabetForm()

    return render(request, 'dashbord/dashbord.html',
                  {'running': running, 'start_button_text': "Start Process", 'word_label': word_label, 'form': form})


# Other imports...

from django.shortcuts import render, redirect, get_object_or_404
from .models import RecognizedAlphabet
from .forms import RecognizedAlphabetForm
import requests
from django.http import HttpResponse

# Other imports...
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .models import RecognizedAlphabet  # Adjust this import based on your project structure




def pay(request, id):
    # Get the recognized alphabet based on the provided ID
    recognized_alphabets = RecognizedAlphabet.objects.get(id=id)

    if request.method == "POST":
        # Get necessary payment details from the form
        phone = request.POST['phone']
        amount = float(recognized_alphabets.price)  # Convert Decimal to float

        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        payload = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "PYMENT001",
            "TransactionDesc": "School fees"
        }

        # Make the Mpesa API request
        response = requests.post(api_url, json=payload, headers=headers)

        # Process the response
        if response.status_code == 200:
            # Payment request successful, redirect to download URL
            return redirect('download-url')  # Adjust 'download_url' to your actual download URL route name
        else:
            return HttpResponse('Payment request failed')

    return render(request, 'dashbord/pay.html', {'recognized_alphabets': recognized_alphabets})

def recognize_letters(request):
    return render(request, 'dashbord/recognized-letters.html')


def download(request):
    return render(request,'dashbord/download-pdf.html')



from django.shortcuts import render
from django.http import JsonResponse


def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        # Perform chatbot logic here

        # Example response
        chatbot_response = "This is a response from the chatbot."

        return JsonResponse({'response': chatbot_response})

    return render(request, 'dashbord/chat.html')  # Render the template for GET requests


# views.py
from django.shortcuts import render

def user_list(request):
    # Assuming users is a list of dictionaries
    users = [
        {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
        {'id': 2, 'username': 'user2', 'email': 'user2@example.com'},
        # Add more user dictionaries as needed
    ]
    return render(request, 'auth/register.html', {'users': users})

