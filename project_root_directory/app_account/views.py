"""
Views for the app_account app.
"""
from django.shortcuts import redirect, render
from django.contrib.auth import (
    authenticate, login as auth_login, logout as auth_logout, get_user_model)
from django.contrib import messages
from django.urls import reverse


def view_login(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                raise ValueError("Both email and password are required")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                print('here')
                return redirect(reverse('app_chatbot:ui_chatbot'))
            else:
                messages.error(request, 'Invalid email or password')
        except ValueError as ve:
            messages.error(request, str(ve))
        except Exception as e:
            print(e)
            messages.error(
                request,
                'An unexpected error occurred. Please try again later.'
            )

    return render(request, 'registration/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = get_user_model().objects.create_user(email, password1)
                user.save()
                auth_login(request, user)
                return redirect(reverse('app_chatbot:ui_chatbot'))
            except Exception as e:
                print(e)
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'registration/register.html')


def logout(request):
    auth_logout(request)
    return redirect(reverse('app_account:login'))
