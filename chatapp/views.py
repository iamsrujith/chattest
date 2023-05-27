import random

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from chatapp.forms import SignupForm
from chatapp.models import User

user = get_user_model()


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                user.is_online = True
                user.save()
                return redirect('home')
    else:
        form = AuthenticationForm()
        form.fields['username'].label = 'Email'

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    user = User.objects.filter(pk=request.user.pk).first()
    user.is_online = False
    user.save()
    logout(request)
    return redirect('login')


# @login_required
# def match_users(request):
#     user = request.user
#     online_users = User.objects.filter(is_online=True).exclude(pk=user.pk)
#     matched_users = online_users.filter(interests__in=user.interests.all())
#
#     if matched_users.exists():
#         matched_user = random.choice(matched_users)
#     else:
#         matched_user = random.choice(online_users)
#
#     # Create a chat room name based on user IDs
#     room_name = f"{user.pk}-{matched_user.pk}"
#     print(room_name)
#
#     # Redirect the users to the chat room
#     self.send(text_data=json.dumps({'redirect': f'/chat/{room_name}'}))


def update_status(request):
    user = request.GET.get("user")
    status = request.GET.get("status")
    if user is not None:
        user = User.objects.get(pk=user)
        if status == "on":
            user.is_online = True
            updated_status = "Online"
        else:
            user.is_online = False
            updated_status = "Offline"
        user.save()

    # Return the updated content as HTTP response
    return HttpResponse(updated_status)


def chat_room(request,id):
    return render(request, 'chat.html')


# views.py

from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

from django.core.cache import cache
from .models import User

def join_chat(request):
    # Fetch the user's interests
    interests = request.session.get('interests', [])

    # Get all active users from the database
    all_users = User.objects.filter(is_online=True)

    # Iterate over the users and find a matching user
    for user in all_users:
        # Check if the user's interests match
        if list(user.interests) == interests:
            # Set the matched user as offline
            user.is_online = False
            user.save()

            # Start the chat session with the matched user
            chat_session_id = create_chat_session(request.user.id, user.id)
            print(chat_session_id)
            return redirect('chat_room', chat_session_id)

    # If no match is found, update the interests of the current user
    user = request.user
    user.interests = interests
    user.save()

    # Render the join chat template
    return render(request, 'chat.html')


import random
import string


def create_chat_session(user_id1, user_id2):
    # Generate a random 10-digit alphanumeric string as the session ID
    session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # Save the session ID in the database or any other storage mechanism of your choice
    # You can associate the session ID with the user IDs or any other relevant data

    return session_id
