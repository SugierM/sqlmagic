from django.shortcuts import render

def tested(request):
    return render(request, 'products.html')


