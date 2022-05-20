from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):
    # pull data
    # transoform
    return render(request,'hello.html',{'name':'Alex'})
    #HttpResponse('Hello World')
