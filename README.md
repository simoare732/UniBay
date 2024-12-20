# E-commerce with Django
An eBay-like website for buying and selling products.

# Requirments
* Python 3.10 or higher
* pipenv 2024.0.1 or higher
```powershell
pip3 install pipenv
```
A virtual environment is created using the following command, and the subshell is opened:
```powershell
pipenv install django
pipenv shell
```
Creating a virtual environment is useful to keep the project isolated.

Now, clone the project:
```powershell
git clone https://github.com/simoare732/ecommerce_django.git
```

Within this environment, install the crispy-forms and bootstrap5 applications, 
which are helpful for enhancing the overall aesthetics of the application:
```powershell
pip install django-crispy-forms
pip install crispy-bootstrap5
```
To use them, you need to add crispy_forms and bootstrap5 to INSTALLED_APPS in the settings.py file.

Next, add the following lines to the settings.py file:
```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```


To support the images that the site will use, install the pillow library:
```powershell
pip install pillow
```
To use this library, simply import it where necessary with the following line:
```python
from PIL import Image
```

Of course, the application is already configured to use these libraries.

As an alternative to the individual commands, you can install all the required libraries using the command:
```powershell
pip install -r requirements.txt
```
Inside the main folder, there is a file called sql.txt that contains SQL code useful for inserting default categories into the database. 
If you want to recreate the database from scratch, copy the content of this file and paste it into a query console of the database.

# Made by
Made by simoare732
Date: 12/20/2024 mm-dd-yyyy
