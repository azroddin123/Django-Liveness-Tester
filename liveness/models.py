from email.policy import default
from pyexpat import model
from django.db import models


# Create your models here.
from django.db import models
from matplotlib.image import thumbnail


class Task(models.Model) :
    folder_path = models.CharField(max_length=70,help_text="folder name with path") 
    total_images = models.IntegerField(help_text="count total images in given folder",default=0)
    skipped_images = models.IntegerField(help_text="akipped image  in given folder",default=0)
    live_images = models.IntegerField(help_text="live image count",default=0)
    spoof_images = models.IntegerField(help_text="spoof images count here",default=0)
    live_percentage = models.FloatField(help_text="percenage count of live images",default=0)
    folder_type = models.CharField(max_length=10,help_text="Spoof or Live")
    processed_image = models.IntegerField(default=0)
    status = models.CharField(max_length=10,help_text="if all image processed complete othrewise incomplete",default="incomplete")
    class Meta :
         db_table = "task"

class Result(models.Model):  
    folder = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True) 
    image_name = models.CharField(max_length=100,help_text="Save image name with path",default=None)  
    type = models.CharField(max_length=15,help_text="sended request to Api has sucess or error",default=None)  
    title = models.CharField(max_length=30,help_text="",default=None)  
    score = models.FloatField(max_length=30,null=True,default=None) 
    label = models.CharField(max_length=30,null=True,default=None)
    prediction_gender = models.CharField(max_length=30,null=True,default=None) 
    confidence_gender = models.CharField(max_length=30,null=True,default=None)
    prediction_age = models.IntegerField(null=True,default=None)      
    confidence_age = models.IntegerField(null=True,default=None)
    show_notification = models.BooleanField(default=False)
    thumbnail  = models.ImageField(upload_to='images',blank=True,default=None)
    thumbnail_img_name = models.CharField(max_length=100,default=None)
    error_message = models.CharField(max_length=50,default=" ",null=True)
    class Meta:  
        db_table = "result"