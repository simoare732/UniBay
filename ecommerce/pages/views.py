from django.shortcuts import render

def home_page(request):
    #login_ok = request.GET.get('login') == 'ok'
    #return render(request, 'pages/home_page.html', context={'title':'Home page', 'login_ok': login_ok})
    return render(request, 'pages/home_page.html')