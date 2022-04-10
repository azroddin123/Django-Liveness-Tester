from pyexpat import model
from django.db import models


# Create your models here.
from django.db import models

class Task(models.Model) :
    folder_path = models.CharField(max_length=70,help_text="folder name with path") 
    total_images = models.IntegerField(help_text="count total images in given folder",default=0)
    skipped_images = models.IntegerField(help_text="akipped image  in given folder",default=0)
    live_images = models.IntegerField(help_text="live image count",default=0)
    spoof_images = models.IntegerField(help_text="spoof images count here",default=0)
    live_percentage = models.FloatField(help_text="percenage count of live images",default=0)
    class Meta :
         db_table = "task"

class Result(models.Model):  
    folder = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True) 
    image_name = models.CharField(max_length=100,help_text="Save image name with path")  
    type = models.CharField(max_length=15,help_text="sended request to Api has sucess or error")  
    title = models.CharField(max_length=30,help_text="")  
    score = models.FloatField(max_length=30,null=True,default=None) 
    label = models.CharField(max_length=30,null=True)
    prediction_gender = models.CharField(max_length=30,null=True) 
    confidence_gender = models.CharField(max_length=30,null=True)
    prediction_age = models.IntegerField()
    confidence_age = models.IntegerField()
    show_notification = models.BooleanField(default=False)
    class Meta:  
        db_table = "result"
        
        
#         from django.db import models



# class Result(models.Model):  
#     folder = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True) 
#     image_name = models.CharField(max_length=100,help_text="Save image name with path")  
#     type = models.CharField(max_length=15,help_text="sended request to Api has sucess or error")  
#     title = models.CharField(max_length=30,help_text="")  
#     score = models.FloatField(max_length=30,null=True,default=None) 
#     label = models.CharField(max_length=30,null=True)
#     prediction_gender = models.CharField(max_length=30,null=True) 
#     confidence_gender = models.CharField(max_length=30,null=True)
#     prediction_age = models.IntegerField()
#     confidence_age = models.IntegerField()
#     show_notification = models.BooleanField(default=False)
#     class Meta:  
#         db_table = "result"
        