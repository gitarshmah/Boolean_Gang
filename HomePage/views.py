from django.shortcuts import render

from .models import Question, Choice

# Get questions and display them


def index(request):
    return render(request, 'HomePage/index.html')
