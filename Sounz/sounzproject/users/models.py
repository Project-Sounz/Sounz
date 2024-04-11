from django.db import models

# Create your models here.

class UserDB(models.Model):
    uid=models.IntegerField(max_length=10,primary_key=True)
    username=models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    email = models.EmailField()
    prof_picaddress=models.CharField(max_length=100)
    user_bio=models.TextField()
    phone=models.IntegerField()
    specialised=models.CharField(max_length=40)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> int:
        return self.uid
    
class SavedDB(models.Model):
    uid=models.ForeignKey('UserDB',on_delete=models.CASCADE)
    pid=models.ForeignKey('PostDB',on_delete=models.CASCADE)    
    
class CollabDB(models.Model):
    col_id=models.IntegerField(max_length=10,primary_key=True)
    uid=models.ForeignKey('UserDB',on_delete=models.CASCADE)
    pid=models.ForeignKey('PostDB',on_delete=models.CASCADE)     


