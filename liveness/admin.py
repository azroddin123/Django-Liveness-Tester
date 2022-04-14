from django.contrib import admin
from .models import Task,Result
class AdminTask(admin.ModelAdmin):
    model = Task
    list_display = ('id', 'folder_path','live_percentage','total_images')

class AdminResult(admin.ModelAdmin):
    model = Task
    list_display = ('id', 'folder_id','thumbnail_img_name','score')
admin.site.register(Task,AdminTask)
admin.site.register(Result,AdminResult)



# admin.site.register(Task)

# Register your models here.
# class Task :
#     pass

# class Result :
# #     pass

# admin.site.register(Task)

