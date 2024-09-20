from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, EditUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from .models import Institution, Category, Donation
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')


        if not User.objects.filter(email=email).exists():
            return redirect('register')


        user = authenticate(request, username=email, password=password)

        if user is not None:

            login(request, user)
            return redirect('landing_page')
        else:

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
    # Pobieramy wszystkie darowizny przypisane do zalogowanego użytkownika
    donations = Donation.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'user': request.user, 'donations': donations})


def add_donation_view(request):
    categories = Category.objects.all()
    institutions = Institution.objects.all()
    context = {
        'categories': categories,
        'institutions': institutions,
    }
    return render(request, 'form.html', context)


@login_required
def edit_user_view(request):
    user = request.user
    user_form = EditUserForm(instance=user)
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        if 'save_user' in request.POST:
            user_form = EditUserForm(request.POST, instance=user)
            if user_form.is_valid():
                if user.check_password(request.POST.get('password')):
                    user_form.save()
                    messages.success(request, 'Dane zostały zaktualizowane pomyślnie.')
                    return redirect('landing_page')
                else:
                    user_form.add_error('password', 'Niepoprawne hasło')
                return redirect('edit_user')

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Hasło zostało zmienione pomyślnie.')
                return redirect('landing_page')

    return render(request, 'edit_user.html', {
        'user_form': user_form,
        'password_form': password_form
    })


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

