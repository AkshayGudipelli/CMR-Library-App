from django.shortcuts import render, redirect
from .forms import CollegeUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check if the email exists
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return render(request, 'html/login.html')

        # Authenticate using username (since Django's default auth uses username)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'html/login.html')

    return render(request, 'html/login.html')

    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'html/dashboard.html', {
        'user' : request.user,
    })