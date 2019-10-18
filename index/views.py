from django.shortcuts import render
from api import alogrithm


# Create your views here.
def index(request):
    return render(request, 'index/index.html')
