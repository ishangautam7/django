from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    """Home page view - demonstrates HttpRequest and HttpResponse"""
    return render(request, 'tasks/home.html')


def about(request):
    """About page view"""
    return render(request, 'tasks/about.html')
