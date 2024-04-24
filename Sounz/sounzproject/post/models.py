from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.


class Postdata(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username=models.OneToOneField(User,on_delete=models.CASCADE,default=0)
    media_address = models.CharField(max_length=256)
    likes_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=32, null=True)
    media_type = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    descr = models.TextField()
    lang = models.CharField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pid)


