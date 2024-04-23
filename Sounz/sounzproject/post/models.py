from django.db import models
#from users import models as usermod


# Create your models here.


class Postdata(models.Model):
    pid = models.IntegerField(primary_key=True, default=0)
    #uid = models.ForeignKey(to=usermod.userdata, on_delete=models.CASCADE)
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


