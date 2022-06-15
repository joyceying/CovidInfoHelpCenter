from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "index.html")

def index(request):
    return render(request, "Home.html")

def selftest(request):
    return render(request, "Self-test.html")

def uploadreport(request):
    return render(request, "Upload-Report.html")

