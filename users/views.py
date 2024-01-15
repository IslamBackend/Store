from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from users.froms import RegisterForm, LoginForm


def register_view(request):
    if request.method == 'GET':
        context = {
            'form': RegisterForm
        }
        return render(request, 'users/register.html', context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('/users/login/')
        else:
            return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'GET':
        context = {
            'form': LoginForm
        }
        return render(request, 'users/auth.html', context)
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/users/profile/')
            else:
                form.add_error('username', 'Username or password is incorrect!')

        return render(request, 'users/auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html', {'user': request.user})  # AnonymousUser | User
