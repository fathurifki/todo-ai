from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout
from .forms import UserCreationForm
from django.shortcuts import redirect
from django.db import connection
from django.http import JsonResponse

User = get_user_model()

def index(request):
    """
    View function for home page of site.
    """
    # Generate a simple context to pass to the template rendering engine.
    context = {
        'title': 'Home Page',
        'heading': 'Welcome to the Todo Application',
    }
    
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'landing/index.html', context=context)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            return  render(request, 'register/index.html', {'form': form})
    else:
        form = UserCreationForm()
        request.session.flush()
        return render(request, 'register/index.html', {'form': form})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, password FROM users WHERE email=%s", [email])
            user = cursor.fetchone()

        if user is not None:
            user_id, stored_password = user
            if check_password(password, stored_password):
                user_obj = User.objects.get(pk=user_id)
                auth_login(request, user_obj)
                return redirect('todos/list')  # Redirect to a home page or dashboard after login
            else:
                return render(request, 'login/index.html', {'error': 'Invalid password'})
        else:
            return render(request, 'login/index.html', {'error': 'User not found'})
    elif request.method == 'GET':
        if (request.user.is_authenticated):
            return redirect('todos/list')
        
    return render(request, 'login/index.html')

def logout_user(request):
    if request.method == 'GET':
        logout(request)
        request.session.flush()
        return redirect('login')
    return render(request, 'login/index.html')
