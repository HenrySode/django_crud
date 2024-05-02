from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from . models import Record

# Create your views here.
# -Home page
def home(request):
    return render(request,'webapp/index.html')

# - Create a user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Succesfully account created')
            return redirect('login')
    
    context = {'form':form}
    return render(request, 'webapp/register.html', context)



# -Login a user
def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
                
    
    context = {'form':form}

    return render(request, 'webapp/login.html', context)

#read records
#Dashboard
@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()
    context = {'records': records}
    return render(request, 'webapp/dashboard.html', context=context)

#create records
@login_required(login_url='login')
def create_record(request):
    form = CreateRecordForm()

    if request.method == 'POST':
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your record was added')
            return redirect('dashboard')
        
    context = {'form':form}
    return render(request, 'webapp/create-record.html', context = context)


#update records
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request,'Your record was updated')
            return redirect("dashboard")

    context = {'form':form} 
    return render(request, 'webapp/update-record.html', context=context)

#Read single record
@login_required(login_url='login')
def view_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record':all_records}
    return render(request, 'webapp/view-record.html',context=context)

#delete
@login_required(login_url='login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,'Record deleted')
    return redirect("dashboard")
    

# user logout
def logout(request):
    auth.logout(request)
    messages.success(request,'Logout success!')
    return redirect('login')