from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from .models import BankAccount
from .forms import BankAccountForm




    
def main(request):
    if request.user.is_authenticated:
        current_user = request.user
        account_exit=BankAccount.objects.filter(username=current_user).exists()
        if account_exit:
            data=BankAccount.objects.get(username=current_user)
            
            return render(request,'main.html',{'data':data})
      
    return render(request,'main.html')

@login_required
def homebase(request):
    if request.method == 'POST':
        
        current_user=request.user
        form = BankAccountForm(request.POST)
        
        username = request.POST.get('username')
        if current_user.username==username:
           if form.is_valid():
            
               form.save()
           
               data=BankAccount.objects.get(username=current_user)
            
               return render(request,'main.html',{'data':data})
        messages.info(request,'check account no and username ')
            

    form = BankAccountForm()
    return render(request, 'homebase.html', {'form': form})


def logout(request):
    
    auth_logout(request)
    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        current_user = request.user
        existing_account = BankAccount.objects.filter(username=current_user.username).exists()

        if existing_account:
            return redirect('main')
        return redirect('homebase')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                
                auth_login(request, user)
                current_user = request.user
                existing_account = BankAccount.objects.filter(username=current_user.username).exists()

                if existing_account:
                    return redirect('main')
                else:
                    return redirect('homebase')
            else:
                messages.info(request,'username or password is incorrect')
                return redirect('login')

    return render(request,'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('homebase')
    else:
        form=CreateUserForm()
        if request.method == 'POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Account was created '+ user)
                return redirect('login')
                
        context={'form':form}
    
    return render(request,'register.html',context)






def home(request):
    if request.user.is_authenticated:
        current_user = request.user
        existing_account = BankAccount.objects.filter(username=current_user.username).exists()
        if existing_account:
            return redirect('main')
        else:
            return redirect('homebase')
    return render(request,'home.html')