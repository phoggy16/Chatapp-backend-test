from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Group(models.Model):
    ref_user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Members(models.Model):
    ref_group=models.ForeignKey(Group,on_delete=models.CASCADE)
    members=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Messages(models.Model):
    ref_user=models.ForeignKey(User,on_delete=models.CASCADE)
    ref_group=models.ForeignKey(Group,on_delete=models.CASCADE)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MessageLike(models.Model):
    ref_message = models.ForeignKey(Messages,on_delete=models.CASCADE)
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
