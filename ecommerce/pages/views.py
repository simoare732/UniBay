from django.shortcuts import render
from listings.models import Category, Product
from .filters import ProductFilter

def home_page(request):
    categories = Category.objects.all()
    return render(request, 'pages/home_page.html', {'categories': categories})


'''def search_results(request):
    category = request.GET.get('category')
    query = request.GET.get('query')
    filter = request.GET.get('filter')

    # Per il filtro ho pensato di fare una funzione a parte che do in input il filtro selezionato e restituisce l'ordine richiesto
    # Che poi metterò in orderBy'''


def list_products(request):
    product_filter = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'pages/list_products.html', {'filter': product_filter})

