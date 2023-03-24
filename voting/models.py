from email.policy import default
from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

import uuid#this helps us get a unique id for each of the posts
from datetime import datetime

from voting.manager import UserManager

# Create your models here.
class StudentData(AbstractUser):
    # student = models.ForeignKey(Student, on_delete = models.CASCADE)
    USERNAME_FIELD = 'matric_no'
    # REQUIRED_FIELDS = ['email']
    objects = UserManager()
    student_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    matric_no = models.CharField(max_length=20, unique=True, null=True)
    password = models.CharField(max_length=50, null=True)
    profileimg = models.ImageField(upload_to = 'profile_images', default = 'blank-profile-picture.png')
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    lvl = models.CharField(max_length=20)
    voted = models.CharField(max_length=12, default='no')

    def __str__(self):
        return self.matric_no

class Position(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    name = models.CharField(max_length=50)
    total_vote = models.IntegerField(default=0, editable=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Candidate Pic", upload_to='images/', default = 'blank-profile-picture.png')

    def __str__(self):
        return "{} - {} - {} Votes".format(self.name, self.position.title, self.total_vote)

class Voted(models.Model):
    matric_no = models.CharField(max_length=20)

    def __str__(self):
        return self.matric_no