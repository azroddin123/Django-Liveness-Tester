
from django.shortcuts import redirect, render
from .forms import TaskForm
from .models import Task,Result
# extra package to call api 
import requests
import json
from nb_utils.file_dir_handling import list_files ## pip install nb_utils
import os 



url = "https://live.accurascan.com/upload.php"
payload={}
headers = {}

def get(request) :
    if request.method == "POST":  
        form = TaskForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except: 
                # print("exception occured")
                pass  
        else:
            print("exception occured")
            form = TaskForm()
            return render(request,'index.html',{'form' : form})
    else:  
        form = TaskForm()  
        return render(request,'index.html',{'form':form})  
    
    
    
def show(request):  
    # Here we can show all our folder_path  list
    tasks = Task.objects.all()  
    return render(request,"show.html",{'tasks':tasks})  


def test(request,id):  
    # Here we can process our data and store data  in both the database
    task = Task.objects.get(id=id) 
    print(id)
    # check path of the images folder exists or not 
    dir_path = task.folder_path 
    if os.path.exists(dir_path) == False :
       return render(request,'error.html')
   
    # check folder_id  exist in the  Result model or not  :
    if Result.objects.filter(folder_id=id).exists():
         print(id)
         print("Already process  folder ")
         task = Task.objects.get(id = id)
         results = Result.objects.all().filter(folder_id=id)
         return render(request,'result.html',{'task' : task,'results' : results})
   
    
    image_data = list_files(dir_path, filter_ext=[".png", ".jpg", ".jpeg"])
    # These fields can be used to store the result in task table
    total_image_count = len(image_data)
    skip_count = 0     
    live = 0 
    spoof = 0 
    # Traversing images for testing
    for image in image_data :
        files=[
            # ('photo',('file',open('/home/azhar/liveness_test/11.png','rb'),'image/png')),
        ('photo',(os.path.basename(image),open(image,'rb'),'image/jpg'))
        ]
        response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
        data = json.loads(response.text)
        if data['type'] == "error" :
            print("skipping")
            skip_count = skip_count + 1 
        else :
            img = image
            type = data['type']
            title = data['title']
            score  = data['score']
            label = data['label']
            # checking image label type 
            if label ==  "spoof" : spoof +=  1  
            else : live += 1 
            prediction_gender = data['prediction_gender']
            confidence_gender = data['confidence_gender']
            prediction_age = data['prediction_age']
            confidence_age = data['confidence_age']
            notification = data['show_notification']
            print(img,type,title,score,label,prediction_age,prediction_gender,confidence_gender,confidence_age,label)
            # Storing result of each single image 
            Result.objects.create(image_name=img,type=type,title=title,score=score,label=label,prediction_gender=prediction_gender,confidence_gender=confidence_gender,prediction_age=prediction_age,confidence_age=confidence_age,show_notification=notification,folder_id=id)
    p = round((live / (total_image_count - skip_count ) * 100),2)
    print(f"  Total images : {total_image_count}\n  Skipped Image : {skip_count} \n Live images :  {live} \n  Spoof Images : {spoof} \n Perccent : {p}")
    Result.objects.all().filter(folder_id = id)
    Task.objects.filter(id=id).update(skipped_images=skip_count,total_images=total_image_count,live_images=live,spoof_images=spoof,live_percentage=p)
    task = Task.objects.get(id = id)
    return render(request,'result.html',{'task' : task})
   
def edit(request, id):  
    task = Task.objects.get(id=id)  
    return render(request,'edit.html', {'task':task}) 

# def get_result(request) :
#     result = Result.objects.get(folder=id) 
    
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




def update(request, id):  
    task = Task.objects.get(id=id)  
    form = TaskForm(request.POST, instance = task )  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'task': task})  

# def destroy(request, id):  
#     Task = Task.objects.get(id=id)  
#     Task.delete()  
#     return redirect("/show")  
            