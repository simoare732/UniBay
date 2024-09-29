# E-commerce with Django
Sito web ebay-like per vendere e comprare prodotti

# Requirments
* Python 3.10 or higher
* pipenv 2024.0.1 or higher
```powershell
pip3 install pipenv
```
E' utile creare un ambiente virtuale per mantenere il progetto isolato
Dopo aver clonato il progetto 
```powershell
git clone https://github.com/simoare732/ecommerce_django.git
```
Si crea un ambiente virtuale tramite il comando e si apre la subshell 
```powershell
pipenv install django
pipenv shell
```
Ora all'interno di questo ambiente si installa l'applicazione crispy-forms e bootstrap5 per l'estetica
```powershell
pip install django-crispy-forms
pip install crispy-bootstrap5
```
Per supportare le immagini dei prodotti si installa pillow
```powershell
pip install Pillow
```
Per un'interfaccia più moderna per le categorie si installa django-mptt
```powershell
pip install django-select2
```