from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    
    user=request.user

    if request.user.groups.filter(name="Admin").exists():
        return HttpResponse("Admin Dashboard.Manage all the team here.")
    elif request.user.groups.filter(name="Manager").exists():
        return HttpResponse("Manager's Dashboard.Manage Membersy here.")
    else:
        return HttpResponse("Member Dashboard.Manage your tasks here.")
