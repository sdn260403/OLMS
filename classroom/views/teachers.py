from django.forms.formsets import formset_factory
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import TeachLeaveAppForm,TeacherSignUpForm,TeachLeaveAppForm,AppStatusForm
from ..models import  User,Teacher,StudentLeaveApp,Student,TeachLeaveApp


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers')

#def TeachLeaveApp(request):

#    form = StdLeaveAppForm(request.POST)

 #   if form.is_valid():
  #      form.save()

  #  context = {'form':form}

   # return render(request,'stApp.html',context)


def ShowApp(request): # It will show all application send from students
    teacher = Teacher.objects.filter(user=request.user).first()
    stud = StudentLeaveApp.objects.filter(to_teacher = teacher).all()
    if request.method == 'POST':
        form = AppStatusForm(request.POST)#validating data
        if form.is_valid():
                instance = form.save(commit=False)
                U=request.POST.getlist('id')
                status=request.POST.getlist('status')
                for i in range(len(U)):
                        x=StudentLeaveApp.objects.get(id=U[i])
                        x.status=status[i]
                        x.save()
                
                return redirect('Showapp')#redirect to home page
        else:
                print("INVALID DATA")
         
    form=AppStatusForm()           

    context = {'app':form,'app2':stud}

    return render(request,'ShowApp.html',context)


def Tpage(request):

    context = locals()

    return render(request,'tpage.html',context)


def TLeaveApp(request): 
    flag=0   
    if request.method == 'POST':
        form = TeachLeaveAppForm(request.POST)#validating data
        if form.is_valid() and not request.POST.get('s_date')>request.POST.get('e_date'):
                #saving in Database
                instance = form.save(commit=False)
                teacher = Teacher.objects.filter(user=request.user).first()
                instance.user = teacher
                instance.save()
                return redirect('home')#redirect to home page
        else:
                flag=1 
    else:
        form = TeachLeaveAppForm()                   

    context = {'form':form,'error':flag}

    return render(request,'tApp.html',context)
    
def LA(request):

    teacher = Teacher.objects.filter(user=request.user).first()
    
    d1=[]
    d2=[]
    d3=[]
    
    d1.append(TeachLeaveApp.objects.filter(user=teacher,leaveT="Vacation").count())
    d1.append(TeachLeaveApp.objects.filter(user=teacher,leaveT="Sick Leave").count())
    d1.append(TeachLeaveApp.objects.filter(user=teacher,leaveT="Personal Leave").count())
    
    d2.append(TeachLeaveApp.objects.filter(user=teacher,status="Accepted").count())
    d2.append(TeachLeaveApp.objects.filter(user=teacher,status="Rejected").count())
    d2.append(TeachLeaveApp.objects.filter(user=teacher,status="Pending").count())
    
    d3.append(StudentLeaveApp.objects.filter(to_teacher=teacher,leaveT="Vacation").count())
    d3.append(StudentLeaveApp.objects.filter(to_teacher=teacher,leaveT="Sick Leave").count())
    
    context = { 'ld':d1 , 'pd':d2 ,'sld':d3}
    
    return render(request,'TeacherAnalysis.html',context)

def TeacherStatusOfApp(request):

    teacher = Teacher.objects.filter(user=request.user).first()

    app = TeachLeaveApp.objects.filter(user=teacher).all()

    context = { 'app':app }

    return render(request,'TeacherAppStatus.html',context)


