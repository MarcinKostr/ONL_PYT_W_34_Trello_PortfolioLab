from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm




def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Tworzymy nowego użytkownika
            user = User.objects.create(
                username=form.cleaned_data['email'],  # email jako username
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']  # Hasło będzie hashowane przez formularz
            )
            user.set_password(form.cleaned_data['password'])  # Hashowanie hasła
            user.save()
            return redirect('login')  # Przekierowanie na stronę logowania
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def add_donation_view(request):
    if request.method == 'GET':
        return render(request, 'form.html')

def landing_page_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')
# Create your views here.
