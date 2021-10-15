# E-Commerce
This E-Commerece Project gives general glimes of commerical shopping site where a user can make purchase of his/her requirements under different categories,can view thier purchase history and order status while they can also add products to their carts for later purchase.

# Requirments (Prerequisites)
* python version - 3.0 
* Django version - 3.2
* Djongo version - 1.3
* redis-server version - 6.0
* celery - 5.1
* pillow - 8.3 


# Installation 

Step By Step Installation Guide.

1. Clone the project

   git clone https://github.com/JapDave/E-Commerce.git

2. Make sure you are in E-Commerce folder

3. Install all dependencies

   pip install -r requirements.txt

4. Install mongodb for your system.

5. Create Database in mongodb and you can update your database name and url in your settings.py 

  DATABASES = {

    'default': {
        'ENGINE': 'djongo',
        'NAME': 'Database Name' ,
        'HOST':'Your Database Url',        
    }
}

6. After Connecting to the Database you can migrate by following commands.

   python manage.py makemigrations  
   python manage.py migrate
  
7. Run Server

   python manage.py runserver

8. Now you are ready to use this project.
  