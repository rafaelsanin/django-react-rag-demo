"""
Views for the app_chatbot app.
"""
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app_core.models import Chat
from .utils.graph import respond


@login_required
def ui_chatbot(request):
    chats = list(Chat.objects.filter(
        user=request.user).values("message", "response", "created_at"))
    context = {
        'chats': chats,
    }
    if request.method == 'POST':
        message = request.POST.get('message')
        response = respond(message)

        chat = Chat(user=request.user, message=message,
                    response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'react_chatbot.html', context)


@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = respond(message)

        chat = Chat(user=request.user, message=message,
                    response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'dtl_chatbot.html', {'chats': chats})
