from django.db import models

# Create your models here.

class PostDB(models.Model):
    pid=models.IntegerField(max_length=10,primary_key = True)
    uid=models.ForeignKey('UserDB',on_delete=models.CASCADE)
    media_address=models.CharField(max_length=256)
    likescount=models.IntegerField(default=0)
    tags=models.CharField(max_length=32,null=True)
    mediatype=models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    descr=models.TextField()
    lang=models.CharField(max_length=10)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self)->int:
        return self.pid


