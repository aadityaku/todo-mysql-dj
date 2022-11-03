from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.views import View
from django.views.generic import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class Home(LoginRequiredMixin,View):
    login_url = '/login-user/'
    def get(self,request,id=None):
        if id !=None:
            to=Todo.objects.get(pk=id)
            if to.status == False:
                to.status = True
                to.save()
                return redirect("home")
            else:
                to.status = False
                to.save()
                return redirect("home")
        todo=Todo.objects.filter(user=request.user)
        return render(request,"home.html",{"todo":todo})

    def post(self,request):
        to=Todo()
        to.task=request.POST.get('task')
        to.user=request.user
        to.save()
        return redirect("home")

class DeleteTask(LoginRequiredMixin,View):
    login_url='/login-user/'
    def get(self,r,id):
        to=Todo.objects.get(pk=id,user=r.user)
        to.delete()
        return redirect("home")

@login_required(login_url="/login-user/")
def active(r):
    to=Todo.objects.filter(user=r.user,status=False)
    return render(r,"home.html",{"todo":to})

@login_required(login_url="/login-user/")
def inActive(r):
    to=Todo.objects.filter(user=r.user,status=True)
    return render(r,"home.html",{"todo":to})

def loginUser(r):
    userform=AuthenticationForm(r.POST or None)
    if r.method=="POST":
        username=r.POST.get("username")
        password=r.POST.get("password")
        user = authenticate(username=username,password=password)
        login(r,user)
        return redirect("home")
    return render(r,"login.html",{"userform":userform})


def register(r):
    userform=UserCreationForm(r.POST or None)
    if r.method == "POST":
        if userform.is_valid():
            userform.save()
            username=userform.cleaned_data.get("username")
            password=userform.cleaned_data.get("password1")
            user=authenticate(username=username,password=password)
            login(r,user)
            return redirect("home")
    return render(r,"register.html",{"userform":userform})

def logoutUser(r):
    logout(r)
    return redirect("login")