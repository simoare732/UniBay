# E-commerce with Django
Sito web ebay-like per vendere e comprare prodotti

# Requirments
* Python 3.10 or higher
* pipenv 2024.0.1 or higher
```powershell
pip3 install pipenv
```
Si crea un ambiente virtuale tramite il comando e si apre la subshell 
```powershell
pipenv install django
pipenv shell
```
E' utile infatti creare un ambiente virtuale per mantenere il progetto isolato 

Si cloni ora il progetto 
```powershell
git clone https://github.com/simoare732/ecommerce_django.git
```

Ora all'interno di questo ambiente si installa l'applicazione crispy-forms e bootstrap5, utili per migliorare l'estetica
generale dell'applicazione.
```powershell
pip install django-crispy-forms
pip install crispy-bootstrap5
```
Per poterle utilizzare è necessario aggiungere crispy_forms e bootstrap5 alle INSTALLED_APPS nel file settings.py.

Successivamente è necessario aggiungere le seguenti righe nel file settings.py
```python
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```


Per supportare le immagini che il sito utilizzera si installa pillow
```powershell
pip install pillow
```
Per utilizzare questa libreria è sufficiente aggiungerla dove necessario con la seguente riga
```python
from PIL import Image
```

Chiaramente all'interno dell'applicazione è già tutto predisposto per l'utilizzo di queste librerie.

In alternativa ai vari comandi è possibile installare tutte le librerie necessarie tramite il comando
```powershell
pip install -r requirements.txt
```

