1.To create a Django application that performs liveness testing follow the following steps.

1. Create a Project
$ django-admin startproject liveness_django

2. Create an App
python3 manage.py startapp liveness

4. Database Setup
Create a database djangodb in mysql, and configure into the settings.py file of django project.

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'liveness',  
        'USER':'root',  
        'PASSWORD':'mysql',  
        'HOST':'localhost',  
        'PORT':'3306'  
    }  
}  


5. Create a Model
1.Task Model
Task models can consist of folder name and total image count

2.Result Model
Result model consist of all the json response we can store on the json side 

6. Create a Model Form
The data which can provided by user can be passed through model form we will create model form for Task only because we are passing only folder name in that model after that the json response we are dumping in the database 

7.




