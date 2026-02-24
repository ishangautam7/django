from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, RegisterForm


def home(request):
    """Home page view - demonstrates sessions (visit counter)"""
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


# ---- Authentication Views ----

def register_view(request):
    """User registration - creates a new account"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})


def login_view(request):
    """User login - authenticates and creates session cookie"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'tasks/login.html', {'error': 'Invalid username or password'})
    return render(request, 'tasks/login.html')


def logout_view(request):
    """User logout - clears session"""
    logout(request)
    return redirect('home')


# ---- CRUD Operations (Protected with @login_required) ----

@login_required(login_url='login')
def task_list(request):
    """READ - List tasks for the logged-in user only (Authorization)"""
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required(login_url='login')
def task_create(request):
    """CREATE - Add a new task using Django ModelForm"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})


@login_required(login_url='login')
def task_update(request, pk):
    """UPDATE - Edit an existing task (only if owned by user)"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})


@login_required(login_url='login')
def task_delete(request, pk):
    """DELETE - Remove a task (only if owned by user)"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
