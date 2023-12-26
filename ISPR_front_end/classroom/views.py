from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView 
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .forms import CustomerForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.core import serializers
from django.conf import settings
import os
from .models import Customer,User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, date
from django.core.exceptions import ValidationError
from . import models
import operator
import itertools
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.hashers import make_password
from bootstrap_modal_forms.generic import (
    BSModalLoginView,
    BSModalFormView,
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from subprocess import run,PIPE
from .forms import FirmwareForm
from .models import Firmware
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from .models import Firmware
from .forms import FirmwareForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data['role']

            if role == 'admin':
                user.is_admin = True
            elif role == 'vendor':
                user.is_vendor = True
            elif role == 'regular':
                user.is_regularuser = True

            user.save()
            login(request, user)
            return redirect('home')  # Replace with the URL you want to redirect to after signup
    else:
        form = SignupForm()

    return render(request, 'dashboard/signup.html', {'form': form})

def edit_firmware(request, firmware_id):
    firmware_record = get_object_or_404(Firmware, id=firmware_id)

    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES, instance=firmware_record)
        if form.is_valid():
            # Use form's save method to handle updates and file changes
            form.save()
            return redirect('firmware_records')
    else:
        form = FirmwareForm(instance=firmware_record)

    return render(request, 'dashboard/edit_records.html', {'form': form, 'firmware_record': firmware_record})

def delete_firmware(request, firmware_id):
    firmware_record = get_object_or_404(Firmware, id=firmware_id)
    firmware_record.delete()
    return redirect('firmware_records')

def firmware_records(request):
    firmware_records = Firmware.objects.all()

    context = {
        'firmware_records': firmware_records,
    }

    return render(request, 'dashboard/show_record.html', context)


def delete_record(request, record_id):
    firmware_record = get_object_or_404(Firmware, id=record_id)

    if request.method == 'POST':
        firmware_record.delete()
        return redirect('firmware_records')

    return render(request, 'dashboard/show_record.html', {'firmware_record': firmware_record})




def home(request):
    return render(request, 'dashboard/Welcome.html')


def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def admin_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials. Please enter Only Admin credentials on this page.")
                return redirect('admin_login')
        else:
            messages.error(request, "This user is not found in database")
            return redirect('admin_login') 
     return render(request, 'dashboard/Admin_login.html')

def vendor_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_vendor:
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials. Please enter Only Vendor credentials on this page.")
                return redirect('vendor_login')
        else:
            messages.error(request, "This user is not found in database")
            return redirect('vendor_login') 
     return render(request, 'dashboard/vendor_login.html')

def user_login(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
         if user.is_regularuser:
        # Successful login for a regular user
           auth.login(request, user)
           return redirect('dashboard')
         else:
        # Incorrect credentials or user doesn't have the is_regularuser role
           messages.error(request, "Invalid credentials. Please enter Only User credentials on this page.")
           return redirect('user_login')  # Assuming 'user_login' is the correct URL name      
        else:
            messages.error(request, "This user is not found in database")
            return redirect('user_login') 
     return render(request, 'dashboard/user.html')

        

def logout_view(request):
    logout(request)
    return redirect('/')                


def add_Firmware(request):
    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect or do something else upon successful form submission
            return redirect('firmware_records')
        else:
            # Form is not valid, handle the error
            print(form.errors)
    else:
        form = FirmwareForm()

    choice = {'form': form}
    return render(request, 'dashboard/add_record.html', choice)




def save_record(request):
    if request.method == 'POST':
        form = FirmwareForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Firmware Registered Successfully')
            return redirect('add_Firmware')  # Redirect to a success page after successful form submission
    else:
        form = FirmwareForm()
    
    firmware_records = Firmware.objects.all()
    return render(request, 'dashboard/add_record.html', {'form': form,'firmware_records': firmware_records})






class UserView(ListView):
    model = User
    template_name = 'dashboard/list_user.html'
    context_object_name = 'users'
    paginate_by = 5

    def get_queryset(self):
        return User.objects.order_by('-id')



class Record(ListView):
    model = Customer
    template_name = 'dashboard/list_record.html'
    context_object_name = 'customers'
    paginate_by = 2
    

   


class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'dashboard/u_update.html'
    form_class = UserForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('users')



class recordReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_record.html'
    firmware_records = Firmware.objects.all()
    


class record1ReadView(BSModalReadView):
    model = Customer
    template_name = 'dashboard/view_record1.html'

class UserReadView(BSModalReadView):
    model = User
    template_name = 'dashboard/view_user.html'

class recordUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle.html'
    form_class = CustomerForm
    success_url = reverse_lazy('vehicle')


class CarUpdateView(BSModalUpdateView):
    model = Customer
    template_name = 'dashboard/update_vehicle2.html'
    form_class = CustomerForm
    success_url = reverse_lazy('listvehicle')



class recordDeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle.html'
    form_class = CustomerForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('Record')



class record1DeleteView(BSModalDeleteView):
    model = Customer
    template_name = 'dashboard/delete_vehicle2.html'
    form_class = CustomerForm
    success_message = 'Success: Data was updated.'
    success_url = reverse_lazy('listvehicle')



class DeleteUser(BSModalDeleteView):
    model = User
    template_name = 'dashboard/delete_user.html'
    success_message = 'Success: Data was deleted.'
    success_url = reverse_lazy('users')



def create(request):
    choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Vendor','Regular_User']
    choice = {'choice': choice}
    if request.method == 'POST':
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            username=request.POST['username']
            userType=request.POST['userType']
            email=request.POST['email']
            password=request.POST['password']
            password = make_password(password)
            print("Hashed Password:", password)
            print("User Type")
            print(userType)
            
            if userType == "Vendor":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_vendor=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')
            
            elif userType == "Admin":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True,is_superuser=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users') 
              
            elif userType == "Regular_User":
                a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_regularuser=True)
                a.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('users')  
            else:
                messages.success(request, 'Member was not created')
                return redirect('users')
    else:
        choice = ['1', '0', 5000, 10000, 15000, 'Register', 'Admin', 'Vendor','Regular_User']
        choice = {'choice': choice}
        return render(request, 'dashboard/add.html', choice)


    
    

