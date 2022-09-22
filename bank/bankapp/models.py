from django.db import models
from datetime import datetime
from django.utils import timezone

class Cust(models.Model):
 custid=models.AutoField(primary_key=True)
 passwd=models.CharField(max_length=15)
 name=models.CharField(max_length=25)
 balance=models.IntegerField(default=0)
 email=models.CharField(max_length=60)
 #open_date=models.DateField(default=datetime.now())
 open_date=models.DateField(default=timezone.now)
 status=models.IntegerField(default=1)

 
class Trans(models.Model):
 transid=models.AutoField(primary_key=True)
 sender=models.ForeignKey(Cust,on_delete=models.RESTRICT)
 receiver=models.IntegerField(default=0)
 amount=models.IntegerField(default=0)
 status=models.IntegerField(default=1 )
 dot=models.DateField(default=timezone.now)
 # str(datetime.now().strftime(frmt))
