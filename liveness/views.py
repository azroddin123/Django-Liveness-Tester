from django.conf import settings 
from django.shortcuts import redirect, render
from pathlib import Path
from .forms import TaskForm
from .models import Task,Result
from PIL import Image,ImageOps
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
        form = TaskForm(request.POST,request.Files)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/show')  
            except: 
                print(" 1 exception occured")
                pass  
        else:
            print("2 exception occured")
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
    # check path of the images folder exists or not 
    dir_path = task.folder_path 
    if os.path.exists(dir_path) == False :
       return render(request,'error.html')
    folder_id = id
    processed = 0 
    # processed_image = task.processed_image
    # check folder_id  exist in the  Result model or not  :
    if Result.objects.filter(folder_id=id).exists() and task.status == "complete" :
         task = Task.objects.get(id=id)
         results = Result.objects.filter(folder_id=id,type="success").order_by('label')
         skipped = Result.objects.filter(folder_id=id,type="error")
         return render(request,'result.html',{'task' : task,'results' : results,'skipped': skipped})
    
    image_data = list_files(dir_path, filter_ext=[".png", ".jpg", ".jpeg"])
    # These fields can be used to store the result in task table
    total_image_count = len(image_data)
    status = "None"
    skip_count = 0    
    live = 0 
    spoof = 0 
    # Traversing images for testing
    image_set = set()
    for image in image_data :
        name = os.path.basename(image)
        
        if Result.objects.filter(folder_id=id,image_name=image) :
           data = Result.objects.distinct().get(folder_id=id,image_name=image)
           processed +=1 
           image_set.add(name)
           if data.label == "spoof" : spoof += 1 
           elif data.label == "live" : live += 1
           else : skip_count += 1 
           print(f"processed : {processed} {name}")
         
        else : 
            # thumbnail image generation.
            thumb_image = Image.open(image)
            thumbnail_path = settings.MEDIA_ROOT + "images/" + str(folder_id)
        
            if not os.path.exists(thumbnail_path) :
                    os.mkdir(thumbnail_path)   
        
            try:
                # Grab orientation value.
                image_exif = thumb_image.getexif()
                print(image_exif)
                image_orientation = image_exif[274]
                if 'error' in  image_orientation:
                    image_orientation = 1 
                # Rotate depending on orientation.
                if image_orientation == 3:
                    rotated = thumb_image.rotate(180)
                if image_orientation == 6:
                    rotated = thumb_image.rotate(-90)
                if image_orientation == 8:
                    rotated = thumb_image.rotate(90)
                rotated.convert('RGB').save(f"{thumbnail_path}/{name}","jpeg")
            except:
                thumb_image.convert('RGB').save(f"{thumbnail_path}/{name}","jpeg")
        
            thumbnail = thumbnail_path + "/" + name
        
            if name in image_set :
                print("request already processed")
                
            else :
                files=[
                #  ('photo',('file',open('/home/azhar/liveness_test/11.png','rb'),'image/png')),
                ('photo',(name,open(image,'rb'),'image/jpg'))
                ]
                response = requests.request("POST", url, headers=headers, data=payload, files=files,verify=False)
                image_set.add(name)
            
            data = json.loads(response.text)
            if data['type'] == "error" :
                print(f"skipping {data}")
                skip_count = skip_count + 1 
                processed = processed + 1 
                Result.objects.create(image_name=image,
                    type=data['type'] ,
                    title=data['title'],
                    error_message = data['text'],
                    folder_id=id,
                    thumbnail=thumbnail,
                    thumbnail_img_name=name)
                print(f"processed : {processed} {name}")
            else :
                img = image
                type = data['type']
                title = data['title']
                score  = data['score']
                label = data['label']
                # checking image label type 
                if label ==  "spoof" : 
                    spoof +=  1
                    processed += 1   
                else : 
                    live += 1
                    processed +=1  
                prediction_gender = data['prediction_gender']
                confidence_gender = data['confidence_gender']
                prediction_age = data['prediction_age']
                confidence_age = data['confidence_age']
                notification = data['show_notification']
                
                # print(f" thumbnail => {thumbnail} ")
                print(img,type,title,score,label)
                # Storing result of each single image 
                Result.objects.create(image_name=img,
                    type=type,
                    title=title,
                    score=score,
                    label=label,
                    prediction_gender=prediction_gender,
                    confidence_gender=confidence_gender,
                    prediction_age=prediction_age,
                    confidence_age=confidence_age,
                    show_notification=notification,
                    folder_id=id,
                    thumbnail=thumbnail,
                    thumbnail_img_name=name,
                    error_message = " ")
                print(f"processed : {processed} {name}")
    try : 
        if task.folder_type == "live" : 
            p = round(( live / (total_image_count - skip_count ) * 100),2)
        else :
            p = round(( spoof / (total_image_count - skip_count ) * 100),2)
        
    except :
        p = 0.00
        print ("Zero Division Error occured")
         
    print(f"Total images : {total_image_count}\n  Processd Images : {processed} \n ,Skipped Image : {skip_count} \n Live images :  {live} \n  Spoof Images : {spoof} \n Perccent : {p}")

    if total_image_count == processed :
        status = "complete"
        
    Result.objects.filter(folder_id = id)
    Task.objects.filter(id=id).update(skipped_images=skip_count,
    total_images=total_image_count,
    live_images=live,
    spoof_images=spoof,
    live_percentage=p,
    folder_type=task.folder_type,
    processed_image = processed,
    status = status)
    task = Task.objects.get(id = id)
    results = Result.objects.filter(folder_id=id)
    return render(request,'result.html',{'task' : task,'results':results})

def edit(request, id):  
    task = Task.objects.get(id=id)  
    return render(request,'edit.html', {'task':task}) 

def update(request, id):  
    task = Task.objects.get(id=id)  
    form = TaskForm(request.POST, instance = task )  
    if form.is_valid():  
        form.save()  
        return redirect("/show")  
    return render(request, 'edit.html', {'task': task})  

# To edit folder in any case you want to delere 
def destroy(request, id):  
    task = Task.objects.get(id=id)  
    task.delete()  
    return redirect("/show")  
         
 
        
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
             # thumbnail_path = settings.MEDIA_ROOT + "images/" + str(folder_id)
        # print(thumbnail_path)
        # if not os.path.exists(thumbnail_path) :
        #         os.mkdir(thumbnail_path)
    
        # thumbnail_image = Image.open(image)
        
        # p = Path(image)
        
        # thumbnail_image.resize((200,200),Image.ANTIALIAS)
        # thumbnail_image = thumbnail_image.rotate(-90,expand=1)
        # thumbnail_image.info["exif"] = thumbnail_image.getexif()
        # print(thumbnail_image.getexif())
        
        # thumbnail_image =  ImageOps.exif_transpose(thumbnail_image)
        # thumbnail_image.thumbnail((100,100), Image.ANTIALIAS)
        # thumbnail_image.save(f"{thumbnail_path}/{p.stem}","JPEG")