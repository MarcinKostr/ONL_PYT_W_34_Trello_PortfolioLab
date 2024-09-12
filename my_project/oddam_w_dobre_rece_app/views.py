from django.shortcuts import render




def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')


def add_donation_view(request):
    if request.method == 'GET':
        return render(request, 'form.html')

def landing_page_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')
# Create your views here.
