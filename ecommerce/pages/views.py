from django.shortcuts import render
from listings.models import Category, Product
def home_page(request):
    categories = Category.objects.all()
    return render(request, 'pages/home_page.html', {'categories': categories})


def list_products(request):
    categories = Category.objects.all()
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')  # Valore predefinito per l'ordinamento

    # Filtra i prodotti in base alla categoria e alla query di ricerca
    products = Product.objects.all()

    if category:
        products = products.filter(categories__name=category)

    if query:
        products = products.filter(title__icontains=query)

    # Gestione dell'ordinamento
    if sort_by == 'price-asc':  # Ordina per prezzo crescente
        products = products.order_by('price')
    elif sort_by == 'price-desc':  # Ordina per prezzo decrescente
        products = products.order_by('-price')
    elif sort_by == 'most-sold':  # Ordina per il numero di prodotti venduti
        products = products.order_by('-sold')
    else:
        products = products.order_by('-date')  # Ordinamento predefinito (per data)

    # Restituisci i risultati filtrati tramite richiesta AJAX o renderizza la pagina completa
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'pages/list_products_partial.html', {'products': products, 'categories': categories})

    return render(request, 'pages/list_products.html', {'products': products, 'categories': categories})
