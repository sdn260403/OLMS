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
from ..forms import StdLeaveAppForm,SignUpForm
from ..models import Teacher,Student, User , TeachLeaveApp, StudentLeaveApp


class StudentSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students')

def StLeaveApp(request):
    flag=0
    if request.method == 'POST':
        form = StdLeaveAppForm(request.POST)#validating data
        if form.is_valid() and not request.POST.get('s_date')>request.POST.get('e_date'):
                #saving in Database
                instance = form.save(commit=False)
                student = Student.objects.filter(user=request.user).first()
                instance.user = student
                instance.save()
                return redirect('home')#redirect to home page yyyy-mm-dd
        else:
                flag=1 
    else:
        form = StdLeaveAppForm()                   

    context = {'form':form,'error':flag}

    return render(request,'stApp.html',context)

def StatusOfApp(request):

    student = Student.objects.filter(user=request.user).first()

    app = StudentLeaveApp.objects.filter(user=student).all()

    context = { 'app':app }

    return render(request,'AppStatus.html',context)
    
def LA(request):

    student = Student.objects.filter(user=request.user).first()
    
    d1=[]
    d2=[]
    
    d1.append(StudentLeaveApp.objects.filter(user=student,leaveT="Vacation").count())
    d1.append(StudentLeaveApp.objects.filter(user=student,leaveT="Sick Leave").count())
    
    d2.append(StudentLeaveApp.objects.filter(user=student,status="Accepted").count())
    d2.append(StudentLeaveApp.objects.filter(user=student,status="Rejected").count())
    d2.append(StudentLeaveApp.objects.filter(user=student,status="Pending").count())

    context = { 'ld':d1 , 'pd':d2 }

    return render(request,'StudentAnalysis.html',context)

def Stpage(request):
    return render(request,'stpage.html')
