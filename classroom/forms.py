from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.fields import DateField

from classroom.models import (Student,Teacher,TeachLeaveApp
                                ,StudentLeaveApp ,User, Admin,AppStatus)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','first_name','last_name','Contact_No','email','gender']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        return user


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','first_name','last_name','Contact_No','email','gender']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class AdminSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        student = Admin.objects.create(user=user)
        return user

class AppStatusForm(forms.ModelForm):
    
    class Meta:
        model = StudentLeaveApp
        
        fields = ['status']

class TAppStatusForm(forms.ModelForm):
    
    class Meta:
        model = TeachLeaveApp
        
        fields = ['status']
        

class StdLeaveAppForm(forms.ModelForm):
    class Meta:
        model = StudentLeaveApp

        fields = ['s_date','e_date','leaveT','content', 'to_teacher']
        
        widgets = {
            's_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'e_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        
        }


class TeachLeaveAppForm(forms.ModelForm):
    class Meta:
        model = TeachLeaveApp
        fields = ['s_date','e_date','leaveT','content', 'to_admin']
        widgets = {
            's_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'e_date': forms.widgets.DateInput(attrs={'type': 'date'}),
        
        }
