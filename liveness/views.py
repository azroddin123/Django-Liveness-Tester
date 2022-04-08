
from django.shortcuts import redirect, render
from imageio import save
from matplotlib.font_manager import json_dump
from sklearn.metrics import precision_score
from .forms import TaskForm
from .models import Task,Result


# extra package to call api 


from matplotlib.font_manager import json_dump
import requests
import json
from nb_utils.file_dir_handling import list_files ## pip install nb_utils
import os 



def show(request):  
    tasks = Task.objects.all()  
    return render(request,"show.html",{'tasks':tasks})  


def test(request,id):  
    task = Task.objects.get(id=id) 
    dir_path = task.folder_name
    id = task.id
    image_data = list_files(dir_path, filter_ext=[".png", ".jpg", ".jpeg"])
    for image in image_data :
        url = "https://live.accurascan.com/upload.php"
        payload={}
        files=[
            # ('photo',('file',open('/home/azhar/liveness_test/11.png','rb'),'image/png')),
        ('photo',(os.path.basename(image),open(image,'rb'),'image/jpg'))
        ]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        data = json.loads(response.text)
        skip_count = 0
        if data['type'] == "error" :
            print("skipping")
            skip_count = skip_count + 1 
        else :
            img = image
            type = data['type']
            title = data['title']
            score  = data['score']
            label = data['label']
            prediction_gender = data['prediction_gender']
            confidence_gender = data['confidence_gender']
            prediction_age = data['prediction_age']
            confidence_age = data['confidence_age']
            notification = data['show_notification']
            print(img,type,title,score,label,prediction_age,prediction_gender,confidence_gender,confidence_age,label)
            r_instance = Result.objects.create(image_name=img,type=type,title=title,score=score,label=label,prediction_gender=prediction_gender,confidence_gender=confidence_gender,prediction_age=prediction_age,confidence_age=confidence_age,show_notification=notification)
    count=Result.objects.all(id=id,label="real")
    print(count)
    print("done")
    
    return render(request,'result.html',json.dumps(r_instance))
    
# return render(request,'result.html',)
# Create your views here.
# def get(request) :
#     if request.method == "POST" :
#         form = TaskForm(request.POST) 
#         if form.is_valid() :
#             form.save()
#             return redirect('/show')
#         else:  
#             form = TaskForm()  
#             return render(request,'index.html',{'form':form})  

# def call_api(request,folder_path) :
#     pass


# def edit(request, id):  
#     Task = Task.objects.get(id=id)  
#     return render(request,'edit.html', {'Task':Task})  
# def update(request, id):  
    
#     task = Task.objects.get(id=id)  
#     form = TaskForm(request.POST, instance = Task)  
#     if form.is_valid():  
#         form.save()  
#         return redirect("/show")  
#     return render(request, 'edit.html', {'Task': Task})  
# def destroy(request, id):  
#     Task = Task.objects.get(id=id)  
#     Task.delete()  
#     return redirect("/show")  
            