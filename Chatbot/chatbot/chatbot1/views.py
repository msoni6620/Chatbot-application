from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import auth
import openai
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone 

# # Set the API key
# openai_api_key="API KEY"
# openai.api_key=openai_api_key

# def ask_openai(message):
#     response=openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "user", "content": "You are so helpfull assistant."},
#             {"role":"user","content":message
#             },
#         ]
#     )
#     print(response)
#     answer=response.choices[0].message.content.strip()
#     return answer

# def chatbot(request):
#     chats=Chat.objects.filter(user=request.user)
#     if request.method == "POST":
#         message = request.POST.get('message')
#         response = ask_openai(message)
#         chat=Chat(user=request.user,message=message,response=response,created_at=timezone.now())
#         chat.save()
#         return JsonResponse({'message': message, 'response': response})
#     return render(request, 'chatbot.html')

# Simulated responses dictionary
responses = {
    "hi": "Hello! How can I assist you today?",
    "how are you?": "I'm just a program, but thank you for asking! How about you?",
    "what is your name?": "I'm an AI Chatbot here to assist you.",
    "help": "Of course! Please ask me anything and I'll do my best to help.",
    "bye": "Goodbye! Feel free to come back if you have more questions."
}

def ask_openai(message):
    message_lower = message.lower()
    
    answer = responses.get(message_lower, "I'm sorry, I don't understand that. Can you please rephrase?")
    
    return answer

def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    
    if request.method == "POST":
        message = request.POST.get('message')

        response = ask_openai(message)
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if(request.method =="POST"):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if(user is not None):
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message='Invalid username or password'
            return render(request,'login.html',{'error':error_message})
    # return render(request,'login.html')
    else:
        return render(request,'login.html')

def register(request):
    if(request.method=="POST"):
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2= request.POST['password2']
        if(password1==password2):
            try:
                user=User.objects.create_user(username,email,password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message='Error creating account'
                return render(request,'register.html',{"error_message":error_message})
        else:
            error_message='Password  Dont match'
            return render(request,'register.html',{"error_message":error_message})
    

    
    return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')