from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task


def home(request):
    """Home page view - demonstrates HttpRequest and HttpResponse"""
    return render(request, 'tasks/home.html')


def about(request):
    """About page view"""
    return render(request, 'tasks/about.html')


# ---- CRUD Operations ----

def task_list(request):
    """READ - List all tasks"""
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    """CREATE - Add a new task"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Task.objects.create(title=title, description=description)
        return redirect('task_list')
    return render(request, 'tasks/task_create.html')


def task_update(request, pk):
    """UPDATE - Edit an existing task"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_update.html', {'task': task})


def task_delete(request, pk):
    """DELETE - Remove a task"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
