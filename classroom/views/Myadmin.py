from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from ..decorators import student_required
from ..forms import StdLeaveAppForm,AdminSignUpForm,TAppStatusForm
from ..models import Teacher,Student, User , TeachLeaveApp,Admin, StudentLeaveApp


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_forma.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('adminpage')

def Adpage(request):

    context = {'ad':'Hello'}

    return render(request,'Adpage.html',context)


def ShowTeacherApp(request): # It will show all applications send from teachers
    
    admin = Admin.objects.filter(user=request.user).first()
    teach = TeachLeaveApp.objects.filter(to_admin = admin).all()
    
    if request.method == 'POST':
        form = TAppStatusForm(request.POST)#validating data
        if form.is_valid():
                instance = form.save(commit=False)
                U=request.POST.getlist('id')
                status=request.POST.getlist('status')
                for i in range(len(U)):
                        x=TeachLeaveApp.objects.get(id=U[i])
                        x.status=status[i]
                        x.save()
                
                return redirect('ShowTapp')#redirect to home page
        else:
                print("INVALID DATA")
         
    form=TAppStatusForm()           

    context = {'app':form,'app2':teach}

    return render(request,'showTeacherApp.html',context)
    
    
    
    
    '''app2 = TeachLeaveApp.objects.filter(id=request.POST.get('answer')).all()

    for items in app2:

        items.status = request.POST.get('status')
        items.save()

    context = { 'app':app }

    return render(request,'showTeacherApp.html',context)'''

