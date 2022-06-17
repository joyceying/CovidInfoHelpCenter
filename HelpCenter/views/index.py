from django.shortcuts import render, redirect
from HelpCenter.models import reportDetail
from django.contrib import messages
from django.core.mail import send_mail
from HelpCenter import models
from HelpCenter.views import account
# Create your views here.


def home(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            name, # subject
            message, # message
            email, # from email
            ['ccry1488@gmail.com'], # To email
        )
        return render(request, "index.html", {'name': name})
    else:
        return render(request, "index.html")

def index(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            name,  # subject
            message,  # message
            email,  # from email
            ['ccry1488@gmail.com'],  # To email
        )
        return render(request, "Home.html", {'name': name})
    else:
        return render(request, "Home.html")

def selftest(request):

        report = reportDetail.objects.all()
        context = {'report': report}

        return render(request, "Self-test.html", context)

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



