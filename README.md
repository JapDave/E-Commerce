# E-Commerce

This E-Commerece Project gives general glimes of commerical shopping site where a user can make purchase of his/her requirements under different categories, can view thier purchase history and order status while they can also add products to their carts for later purchase.

# Requirments (Prerequisites)

* [python version - 3.0](https://www.python.org/downloads/)  
* [Django version - 3.2](https://pypi.org/project/Django/) 
* [Djongo version - 1.3](https://pypi.org/project/djongo/)
* [redis-server version - 6.0](https://pypi.org/project/redis-server/)
* [celery - 5.1](https://pypi.org/project/celery/)
* [pillow - 8.3](https://pypi.org/project/Pillow/) 


# Installation 

Step By Step Installation Guide.

1. Clone the project

   ```git clone https://aditetester@bitbucket.org/aditetester/e-commerce.git```

2. Make sure you are in E-Commerce folder

3. Install all dependencies

```
   pip install -r requirements.txt
```

4. Install mongodb for your system.

5. Create Database in mongodb and you can update your database name and url in your settings file.

```
   DATABASES = {
      'default': {
         'ENGINE': 'djongo',
         'NAME': 'Database Name' ,
         'HOST':'Your Database Url',        
      }
   }
```

6. After Connecting to the Database you can migrate by following commands.

   ```
   python manage.py makemigrations 
   python manage.py migrate
   ```
  
7. Run Server

   ```
   python manage.py runserver
   ```

8. Now you are ready to use this project.
  