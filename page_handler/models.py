from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class HOD_model(models.Model):
    HOD_name=models.CharField(max_length=50)
    password=models.CharField(max_length=200)

class course_model(models.Model):
    course_name=models.CharField(max_length=50)
    HOD_undertaken=models.ForeignKey(HOD_model,on_delete=models.SET_NULL,null=True)


class teacher_model(models.Model):
    teacher_name=models.CharField(max_length=50)
    password=models.CharField(max_length=200)
    teacher_course=models.ForeignKey(course_model,on_delete=models.DO_NOTHING)
    HOD=models.ForeignKey(HOD_model,on_delete=models.DO_NOTHING)


class student_model(models.Model):
    student_name=models.CharField(max_length=50)
    password=models.CharField(max_length=200)
    roll_number=models.CharField(max_length=50)
    student_course=models.ForeignKey(course_model,on_delete=models.DO_NOTHING)
    student_head=models.ForeignKey(teacher_model,on_delete=models.DO_NOTHING)

class student_attendance_model(models.Model):
    date_of_attendance=models.DateField()
    student_id=models.ForeignKey(student_model,on_delete=models.DO_NOTHING)
    mark_attendance=models.BooleanField(default=False)

class announcement_model(models.Model):
    title=models.CharField(max_length=200)
    designation=models.CharField(max_length=50)
    announcement=models.CharField(max_length=500)

class book_model(models.Model):
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=50)
    publish_year=models.IntegerField()

class book_issue_model(models.Model):
    username=models.ForeignKey(student_model,on_delete=models.DO_NOTHING)
    book=models.ForeignKey(book_model,on_delete=models.DO_NOTHING)
    date_issued=models.DateField()

class HOD_picture(models.Model):
    HOD=models.ForeignKey(HOD_model,on_delete=models.CASCADE)
    picture=models.ImageField(upload_to="HOD_picture/")

class Teacher_picture(models.Model):
    teacher=models.ForeignKey(teacher_model,on_delete=models.CASCADE)
    picture=models.ImageField(upload_to="Teacher_picture/")

class Student_picture(models.Model):
    student=models.ForeignKey(student_model,on_delete=models.CASCADE)
    picture=models.ImageField(upload_to="Student_picture/")