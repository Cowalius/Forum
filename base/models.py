from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    name=models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Room(models.Model):
    host=models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=150)
    description=models.TextField(null=True,blank=True) #default jest false i by errory wywalalo jakby puste bylo
    participants=models.ManyToManyField(User, related_name="Users", blank=True)
    updated=models.DateTimeField(auto_now=True) #kiedy bedzie save method uzyta to sie odpali
    created= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =["-updated",'-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)#jak pokoj sie usuwa to i wszystkie waidomosci w nim
    body= models.TextField()
    updated = models.DateTimeField(auto_now=True)  # kiedy bedzie save method uzyta to sie odpali
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]