from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    return render(request, 'classroom/home.html')

def Logout(request):

    auth.logout(request)
    return redirect('/')
    
