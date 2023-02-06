from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import InputForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


# def get_name(request):
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             return HttpResponseRedirect('/thanks/')

#     else:
#         form = InputForm()
#     return render(request, 'index.html', {'form': form})


# def register(response):
#     if response.method == "POST":
#         form = InputForm(response.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("/home")
#     else:
#         form = InputForm()
#     return render(response, 'register/index.html', {'form': form})

def index(request):
    return render(request, '/index.html')


def special(request):
    return HttpResponse("You are logged in!")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        inputForm = InputForm(data=request.POST)
        if inputForm.is_valid():
            user = inputForm.save()
            user.set_password(user.password)
            user.save()
        else:
            print(inputForm.errors)
    else:
        inputForm = InputForm()
    return render(request, '/index.html', {'inputForm': inputForm})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your account was inactive')
        else:
            print('Someone tried to login and failed')
            print('They used username: {} and password: {}'.format(
                username, password))
    else:
        return render(request, '/index.html', {})
