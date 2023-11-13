from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
import uuid
from django.core.validators import RegexValidator


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$', message="Up to 10 digits allowed.")
    Contact_No = models.CharField(validators=[phone_regex], max_length=12, blank=True) 
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def getname(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username
   

class StudentLeaveApp(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    to_teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=100,null=True,default='Pending')
    
    s_date=models.DateField()
    e_date=models.DateField()
    lv_choices = (      ('Vacation','Vacation'),
                        ('Sick Leave', 'Sick'),
                        )
    leaveT = models.CharField(max_length=14, choices=lv_choices, default='Vacation')


class AppStatus(models.Model):

    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True,default='Pending')


class TeachLeaveApp(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    to_admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True,default='Pending')
    
    s_date=models.DateField()
    e_date=models.DateField()
    lv_choices = (      ('Vacation','Vacation'),
                        ('Sick Leave', 'Sick Leave'),
                        ('Personal Leave', 'Personal Leave')
                        )
    leaveT = models.CharField(max_length=14, choices=lv_choices, default='Vacation')


