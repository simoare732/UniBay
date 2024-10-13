from django.shortcuts import render
from listings.models import Category, Product
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
    categories = Category.objects.all()
    # Ottieni i parametri GET
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    #filter_option = request.GET.get('filter', '')

    # Filtra i prodotti in base alla categoria e alla query
    products = Product.objects.all()

    if category:
        products = products.filter(categories__name=category)

    if query:
        products = products.filter(title__icontains=query)

    return render(request, 'pages/list_products.html', {'products': products, 'categories': categories})

