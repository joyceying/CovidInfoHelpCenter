from django.shortcuts import render, redirect
from HelpCenter.models import reportDetail
from django.contrib import messages
# Create your views here.


def home(request):
    return render(request, "index.html")

def index(request):
    return render(request, "Home.html")

def selftest(request):
    return render(request, "Self-test.html")

def uploadreport(request):
    if request.method == 'POST':
            saverecord = reportDetail()
            saverecord.date = request.POST.get('date')
            saverecord.symptoms = request.POST.get('symptoms')
            saverecord.closeContact = request.POST.get('closeContact')
            saverecord.name = request.POST.get('name')

            if len(request.FILES) != 0:
                saverecord.image = request.FILES['image']

            saverecord.save()
            messages.success(request, "Upload Successfully")
            return render(request, "Upload-Report.html")

    else:
        return render(request, "Upload-Report.html")

def userprofile(request):
    return render(request, "User-profile.html")



