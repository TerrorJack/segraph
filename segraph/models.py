from django.db import models

class User(models.Model):
    uid=models.IntegerField(primary_key=True)
    username=models.TextField()
    hashed_password=models.TextField()
    salt=models.TextField()
    intro=models.TextField()
    avatar=models.FileField(upload_to='img')
    city=models.TextField()
    contact=models.TextField()

class Gal(models.Model):
    gid=models.IntegerField(primary_key=True)
    galname=models.TextField()

class Pic(models.Model):
    pid=models.IntegerField(primary_key=True)
    time=models.IntegerField()
    user=models.ForeignKey('User')
    gal=models.ForeignKey('Gal')
    content=models.FileField(upload_to='img')
