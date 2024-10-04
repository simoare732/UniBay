from django.shortcuts import render
from listings.models import Category

def home_page(request):
    categories = Category.objects.all()
    return render(request, 'pages/home_page.html', {'categories': categories})