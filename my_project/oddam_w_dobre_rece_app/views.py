from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Institution, Category, Donation
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Sprawdzamy, czy użytkownik istnieje na podstawie adresu e-mail
        if not User.objects.filter(email=email).exists():
            return redirect('register')

        # Uwierzytelnianie użytkownika
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Jeśli uwierzytelnianie się powiedzie
            login(request, user)
            return redirect('landing_page')  # Przekierowanie na stronę główną
        else:
            # Jeśli uwierzytelnianie się nie powiedzie
            return render(request, 'login.html', {'error': 'Błędny login lub hasło'})
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('landing_page')


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



@login_required
def user_profile_view(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})


def add_donation_view(request):
    if request.method == 'GET':
        return render(request, 'form.html')


def landing_page_view(request):
    total_bags = Donation.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    supported_institutions = Donation.objects.values('institution').distinct().count()

    institutions_fundacja = Institution.objects.filter(type=Institution.FOUNDATION)
    institutions_ngo = Institution.objects.filter(type=Institution.NGO)
    institutions_local = Institution.objects.filter(type=Institution.LOCAL_COLLECTION)

    return render(request, 'index.html', {
        'institutions_fundacja': institutions_fundacja,
        'institutions_ngo': institutions_ngo,
        'institutions_local': institutions_local,
        'total_bags': total_bags,
        'supported_institutions': supported_institutions,
    })

