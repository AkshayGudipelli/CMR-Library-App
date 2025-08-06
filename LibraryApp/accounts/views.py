from django.shortcuts import render, redirect
from .forms import CollegeUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CollegeUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created Successfully! ")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CollegeUserCreationForm()
    return render(request, 'html/register.html', {'form': form}) 


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'html/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'html/dashboard.html', {
        'user' : request.user,
    })