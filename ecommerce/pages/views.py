from django.shortcuts import render
from listings.models import Category, Product
def home_page(request):
    categories = Category.objects.all()
    return render(request, 'pages/home_page.html', {'categories': categories})


def list_products(request):
    categories = Category.objects.all()
    category = request.GET.get('category', '')
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'default')

    # Filter products based on the query and category
    products = Product.objects.all()

    if category:
        products = products.filter(categories__name=category)

    if query:
        products = products.filter(title__icontains=query)

    # Manage the sorting of products
    if sort_by == 'price-asc':  # Order by price ascending
        products = products.order_by('price')
    elif sort_by == 'price-desc':  # Order by price descending
        products = products.order_by('-price')
    elif sort_by == 'most-sold':  # Order by most sold
        products = products.order_by('-sold')
    else:
        products = products.order_by('-date')  # Default order (by date)

    # Return the products as a partial view if it's an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'pages/list_products_partial.html', {'products': products, 'categories': categories})

    return render(request, 'pages/list_products.html', {'products': products, 'categories': categories})
