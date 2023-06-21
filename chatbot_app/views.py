import wikipediaapi
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
import django
django.setup()
from django.shortcuts import render, redirect, HttpResponse
from chatbot_app.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pyaiml21 import Kernel
from chatbot_app.models import *
from glob import glob
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk
from gtts import gTTS

import socket
import speech_recognition as sr
import requests
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics  # Add this line
nltk.download('wordnet')


MyBot = Kernel()

aiml_files = glob("AIML FILES/*")
for files in aiml_files:
    MyBot.learn_aiml(files)



def get_ip_address(request):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def predict_gender(name):
    # Load the dataset
    data = pd.read_csv('names_dataset.csv')

    # Remove duplicates (if any)
    data = data.drop_duplicates()

    # Shuffle the dataset
    data = data.sample(frac=1).reset_index(drop=True)

    # Split the dataset into features (X) and labels (y)
    X = data['name']
    y = data['gender']

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the CountVectorizer
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))

    # Fit and transform the training set
    X_train_features = vectorizer.fit_transform(X_train)

    # Transform the testing set
    X_test_features = vectorizer.transform(X_test)

    # Initialize the model
    model = MultinomialNB()

    # Train the model
    model.fit(X_train_features, y_train)

    # Make predictions on the testing set
    y_pred = model.predict(X_test_features)

    # Calculate accuracy
    accuracy = metrics.accuracy_score(y_test, y_pred)

    # Preprocess the input name and transform it into features
    new_name_features = vectorizer.transform([name])

    # Predict the gender of the input name
    predicted_gender = model.predict(new_name_features)

    return predicted_gender[0], accuracy




def speech_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Listen for speech input
        audio = recognizer.listen(source)


# @login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()


# Function to get synonyms for a word
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return list(synonyms)


# Function to lemmatize the input text
def lemmatize_text(text):
    lemmatized_tokens = []
    tokens = text.split()
    for token in tokens:
        lemmatized_tokens.append(lemmatizer.lemmatize(token))
    return ' '.join(lemmatized_tokens)


def get_signed_in_username(request):
    # Retrieve the signed-in user object
    user = request.user
    return user.username

import pyswip


def get_bot_response(request):

    user_input = request.GET.get('user_input')
    speech_input = request.GET.get('speech_input')

    if speech_input == 'true':
        # Speech input was used, so convert speech to text
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            print("User Input:", user_input)
        except sr.UnknownValueError:
            print("Unable to recognize speech")
        except sr.RequestError as e:
            print("Error: ", str(e))

    if user_input.startswith("Guess gender"):
        name = user_input.split("Guess gender", 1)[-1].strip()
        gender, accuracy = predict_gender(name)
        bot_response = f"The predicted gender for the name '{name}' is {gender}."

    elif user_input.lower() == "hello":
        bot_response = f"Hello! How can I assist you today?"

    elif user_input.lower() == "tell my ip":
        user_ip = get_ip_address(request)
        bot_response = "Your IP address is: " + user_ip

    # Rest of your code...

    else:
        wiki = wikipediaapi.Wikipedia('en')
        page = wiki.page(user_input)
        if page.exists():
            content = page.text
            lines = content.split('\n')[:3]  # Limiting to 5 lines
            summary = '\n'.join(lines)
            bot_response = summary
        else:
            aiml_response = MyBot.respond(user_input, "USER_1")
            if aiml_response:
                bot_response = aiml_response












    tts = gTTS(bot_response, lang='en')
    tts.save("bot_response.mp3")
    os.system("bot_response.mp3")

    return render(request, 'home.html', {'user_input': user_input, 'bot_response': bot_response})
def main(request):
    return render(request, 'chat.html')

# def loginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username, password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return  HttpResponse("USERNAME AND PASSWORD ARE INCORRECT !")




    # return render(request, 'login.html')

# def signupPage(request):
#     if request.method=='POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')
#         if pass1 != pass2:
#             return HttpResponse("PASSWORDS DOESN'T MATCHED !")
#         my_user = User.objects.create_user(uname,email,pass1)
#         my_user.save()
#         return redirect('login')




    # return render(request, 'signup.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')



def signup(request):
    user_ip = get_ip_address(request)
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')

        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 != pass2:
            return HttpResponse("PASSWORDS DOESN'T MATCHED !")
        else:
            user = User(name=uname, email=email, password=pass1, ip_address=user_ip)
            user.save()
            user.signed_in.connect(user)
            user.save()

            return redirect('login')
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = User.nodes.filter(name=username, password=pass1).first()
        if user:
            return redirect('home')
        else:
            return HttpResponse("PASSWORD & EMAIL DOESN'T MATCHED !")

    return render(request, 'login.html')