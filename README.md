# E-Commerce

This E-Commerece Project gives general glimes of commerical shopping site where a user can make purchase of his/her requirements under different categories, can view thier purchase history and order status while they can also add products to their carts for later purchase.

# Requirments (Prerequisites)

* [python version - 3.0](https://www.python.org/downloads/), for as backend core language.
* [Django version - 3.2](https://pypi.org/project/Django/), for web framework of python 
* [Djongo version - 1.3](https://pypi.org/project/djongo/), for connecting to mongodb database.
* [redis-server version - 6.0](https://pypi.org/project/redis-server/), for serving message caching.
* [celery - 5.1](https://pypi.org/project/celery/), for queueing task.
* [pillow - 8.3](https://pypi.org/project/Pillow/), for serving image file to python django.


# Installation 

Step By Step Installation Guide.

1. Create an virtual environment for project as virtual environments allows you to avoid installing python packages globally and run multiple instances of web applications on different versions of python and django, on a single machine. [Here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) is a guide on how to install Virtualenv.

   * Before we start, we need to create a virtualenv for our app, so open up your Command Prompt (for Windows) or Terminal (for Mac, Linux) and type the following:
      
      ```
      virtualenv venv
      ```


2. Clone the project.

   ```
   git clone https://aditetester@bitbucket.org/aditetester/e-commerce.git
   ```
   
3. Make sure you are in E-Commerce folder.

4. Install all dependencies into virtual environment.

   ```
   pip install -r requirements.txt
   ```

5. Install mongodb for your system from [here](https://www.mongodb.com/try/download/community).

6. Create database in mongodb and you can update your database name and url in your settings file.

   ```
   DATABASES = {
      'default': {
         'ENGINE': 'djongo',
         'NAME': 'Database Name',
         'HOST':'Your Database Url',        
      }
   }
   ```

7. Create superuser by below command and enter your credential to access admin section.
   
   ```
   python manage.py createsuperuser
   ```

8. After connecting to the database you can migrate by following commands.

   ```
   python manage.py makemigrations 
   python manage.py migrate
   ```
  
9. Run the development server from the terminal by below code.

   ```
   python manage.py runserver
   ```

10. Now you are ready to use this project.

# Deployment 

* As first thing needed for deployment is Procfile file which consists of our wsgi and worker settings which is necessary for deploying our site.

   ```
   web: gunicorn eshop.wsgi --log-file -
   worker: celery -A eshop.celery worker -B --loglevel=info
   ```

* Next important step is for creating runtime.txt file with mentioning our language version.

   ```
   python-3.8.10
   ```

* Now by creating an .env file beside settings.py file and declare all the environment variables needed for our site.

* For serving static files in django, we need to install whitenoise as django does not support serving static files in production, by default. 

   ```
   pip install whitenoise
   ```

* We also need to add whitenoise to our middlewares into settings.py file for letting django to know about whitenoise.

   ```
   MIDDLEWARE = [
      ...
      'whitenoise.middleware.WhiteNoiseMiddleware',
    ]
   ```

* Now you can collect all the static files over folder in one folder by command.

   ```
   django-admin collectstatic
   ```

* Open up settings.py file and make the following changes, preferably at the bottom of the file.
   
   ```
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

* As project is meant to deploy on heroku we needed heroku cli,which you can download as per your system.
   * For unbntu 16+, run the following from your terminal:

      ```
      sudo snap install --classic heroku
      ```

   * you can also check out the documentation [heroku cli.](https://devcenter.heroku.com/articles/heroku-cli)

* Login to heroku cli from terminal through your credientials.

* Create an heroku app with unique name.

   ```
   heroku create shopfreeapp
   ```
   
* By creating app, you can add git remote location and can commit your stage level by -

   ```
   git add .
   git commit -m "Initial commit"
   ```

* After commiting you can push project to heroku by-

   ```
   git push heroku master
   ```