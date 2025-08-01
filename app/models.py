import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class File(models.Model):
    filename = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, default='drscratch')
    coder = models.CharField(max_length=100, default='drscratch')
    # type_user = models.CharField(max_length=100, default='drscratch')
    method = models.CharField(max_length=100)
    batch_id = models.UUIDField(null=True, default=None, editable=False)
    time = models.DateField(auto_now=False)
    language = models.TextField(default="en")
    score = models.IntegerField()
    vanilla_metrics = models.JSONField(default=dict)
    extended_metrics = models.JSONField(default=dict)
    spriteNaming = models.IntegerField()
    backdropNaming = models.IntegerField()
    initialization = models.IntegerField()
    deadCode = models.IntegerField()
    duplicateScript = models.IntegerField()

class BatchCSV(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_time = models.FloatField(default=0)
    filepath = models.CharField(max_length=100)
    num_projects = models.IntegerField()
    max_points = models.FloatField()
    points = models.FloatField()
    max_logic = models.FloatField()
    logic = models.FloatField()
    max_parallelism = models.FloatField()
    parallelism = models.FloatField()
    max_data = models.FloatField()
    data = models.FloatField()
    max_synchronization = models.FloatField()
    synchronization = models.FloatField()
    max_userInteractivity = models.FloatField()
    userInteractivity = models.FloatField()
    max_flowControl = models.FloatField()
    flowControl = models.FloatField()
    max_abstraction = models.FloatField()
    abstraction = models.FloatField()
    max_math_operators = models.FloatField()
    math_operators = models.FloatField()
    max_motion_operators = models.FloatField()
    motion_operators = models.FloatField()
    mastery = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)

class CSVs(models.Model):
    filename = models.CharField(max_length=100)
    directory = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, default='drscratch')
    coder = models.CharField(max_length=100, default='drscratch')
    date = models.DateTimeField(default=datetime.datetime.now)


class Coder(User):
    birthmonth = models.CharField(max_length=100)
    birthyear = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    gender_other = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    img = models.ImageField(upload_to="img/", default="app/images/drScratch.png")


class Organization(User):
    hashkey = models.TextField()
    img = models.ImageField(upload_to="img/", default="app/images/drScratch.png")


class OrganizationHash(models.Model):
    hashkey = models.TextField()


class Comment(models.Model):
    user = models.TextField()
    text = models.TextField()
    date = models.DateField()


class Activity(models.Model):
    text = models.TextField()
    date = models.DateField()


class Discuss(models.Model):
    nick = models.TextField()
    date = models.DateTimeField()
    comment = models.TextField()


class Stats(models.Model):
    daily_score = models.TextField()
    basic = models.TextField(default="")
    development = models.TextField(default="")
    master = models.TextField(default="")
    daily_projects = models.TextField(default="")
    parallelization = models.IntegerField(default=int(0))
    abstraction = models.IntegerField(default=int(0))
    logic = models.IntegerField(default=int(0))
    synchronization = models.IntegerField(default=int(0))
    flowControl = models.IntegerField(default=int(0))
    userInteractivity = models.IntegerField(default=int(0))
    dataRepresentation = models.IntegerField(default=int(0))
    deadCode = models.IntegerField(default=int(0))
    duplicateScript = models.IntegerField(default=int(0))
    spriteNaming = models.IntegerField(default=int(0))
    initialization = models.IntegerField(default=int(0))


class Student(models.Model):
    #student = models.ForeignKey(User, unique=True)
    student = models.OneToOneField(User, on_delete=models.CASCADE)


class Teacher(models.Model):
    #teacher = models.ForeignKey(User, unique=True)
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    hashkey = models.TextField()
    #classroom = models.ManyToManyField(Classroom)
