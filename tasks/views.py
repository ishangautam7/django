from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm


def home(request):
    """Home page view - demonstrates sessions (visit counter)"""
    # Session: track visit count
    visit_count = request.session.get('visit_count', 0)
    visit_count += 1
    request.session['visit_count'] = visit_count

    return render(request, 'tasks/home.html', {'visit_count': visit_count})


def about(request):
    """About page view"""
    return render(request, 'tasks/about.html')


def toggle_theme(request):
    """Toggle theme between light and dark - demonstrates session usage"""
    current_theme = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', '/'))


# ---- CRUD Operations using Django Forms ----

def task_list(request):
    """READ - List all tasks"""
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_create(request):
    """CREATE - Add a new task using Django ModelForm"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})


def task_update(request, pk):
    """UPDATE - Edit an existing task using Django ModelForm"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})


def task_delete(request, pk):
    """DELETE - Remove a task"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
