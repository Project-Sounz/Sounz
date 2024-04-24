from django.db import models
from post.models import Postdata
from django.contrib.auth.models import User
import uuid


# Create your models here.

class userdata(models.Model):
    uid=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    password = models.CharField(max_length=15)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField()
    prof_picaddress=models.ImageField(upload_to='static/images/',null=True,blank=True)
    user_bio=models.TextField()
    phone=models.IntegerField()
    specialised=models.CharField(max_length=40)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> int:
        return self.uid
    
class SavedDB(models.Model):
    uid=models.ForeignKey(to=userdata,on_delete=models.CASCADE)
    pid=models.ForeignKey(to=Postdata,on_delete=models.CASCADE, default=0)    
    
class CollabDB(models.Model):
    col_id=models.IntegerField(primary_key=True)
    uid=models.ForeignKey(to=userdata,on_delete=models.CASCADE)
    pid=models.ForeignKey(to=Postdata,on_delete=models.CASCADE, default=0)     


