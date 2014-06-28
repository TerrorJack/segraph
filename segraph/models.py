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

    @staticmethod
    def next():
        next_uid=0
        if User.objects.count()>0:
            next_uid=User.objects.all().aggregate(models.Max('uid'))['uid__max']+1
        return next_uid

class Gal(models.Model):
    gid=models.IntegerField(primary_key=True)
    galname=models.TextField()

    @staticmethod
    def next():
        next_gid=0
        if Gal.objects.count()>0:
            next_gid=Gal.objects.all().aggregate(models.Max('gid'))['gid__max']+1
        return next_gid

class Pic(models.Model):
    pid=models.IntegerField(primary_key=True)
    time=models.IntegerField()
    user=models.ForeignKey('User')
    gal=models.ForeignKey('Gal')
    content=models.FileField(upload_to='img')

    @staticmethod
    def next():
        next_pid=0
        if Pic.objects.count()>0:
            next_pid=Pic.objects.all().aggregate(models.Max('pid'))['pid__max']+1
        return next_pid
