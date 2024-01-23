from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

from .models import BankAccount
from .forms import BankAccountForm

# views.py
from .models import BankAccount
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from decimal import Decimal

def main(request):
    
    if request.method == 'POST':
        # Retrieve form data
        recipient_account_number = request.POST.get('recipient_account_number')

        # Validate if the account number exists
        try:
            recipient_account = BankAccount.objects.get(account_number=recipient_account_number)
        except BankAccount.DoesNotExist:
            messages.info(request,"Invalid recipient account number")
            return redirect('main')
        # Retrieve the current user's account
        current_user = request.user
        sender_account = BankAccount.objects.get(username=current_user)

        # Retrieve the amount to be transferred
        try:
            amount = Decimal(request.POST.get('amount'))
        except ValueError:
            messages.info(request,"Invalid amount")
            return redirect('main')
        # Check if the user has enough funds
        if recipient_account.account_number == sender_account.account_number:
            messages.info(request,"sender and receier are same")
            return redirect('main')
        if amount <= sender_account.balance and amount>0:
            # Perform the transfer
            sender_account.withdraw(amount)
            recipient_account.deposit(amount)

            # Update the sender's and recipient's data in the database
            sender_account.save()
            recipient_account.save()

            # Add transaction details to sender and recipient accounts
            sender_account.add_transaction('Sent', amount, recipient_account.account_number)
            recipient_account.add_transaction('Received', amount, sender_account.account_number)

            # Redirect to the main page with updated data
            return redirect('main')
        else:
            messages.info(request,"insufficient amount or zero amount")
            return redirect('main')

    # If the request is not a POST request, render the main page
    current_user = request.user
    data = BankAccount.objects.get(username=current_user)
    
    return render(request, 'main.html', {'data': data})






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
        messages.error(request,"username doesn't match or accountno already exist")
            

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
                if user.is_staff:       # Redirect to an admin-specific page
                    return redirect('admin_dashboard')
                
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
        user=request.user
        if user.is_staff:       # Redirect to an admin-specific page
            return redirect('admin_dashboard')
        
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
        user=request.user
        if user.is_staff:       # Redirect to an admin-specific page
            return redirect('admin_dashboard')
        
        current_user = request.user
        existing_account = BankAccount.objects.filter(username=current_user.username).exists()
        if existing_account:
            return redirect('main')
        else:
            return redirect('homebase')
    return render(request,'home.html')





# views.py

from django.shortcuts import render, get_object_or_404
from .models import BankAccount

def admin_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_name = request.POST.get('user_select')
        deposit_amount = request.POST.get('deposit_amount')
        withdrawal_amount = request.POST.get('withdrawal_amount')
        
        if action == 'deposit':
            if not deposit_amount or deposit_amount.strip() == '':
                messages.info(request, "Please enter a valid deposit amount.")
                return redirect('admin_dashboard')
            user=BankAccount.objects.get(username=user_name)
            try:
                deposit_amount = Decimal(deposit_amount)
            except ValueError:
                messages.info(request,'invalid amount')
            if deposit_amount<=0:
                messages.info(request,'invalid amount')
                return redirect('admin_dashboard')    
            user.deposit(deposit_amount)
            user.save()
            messages.info(request,'Amount added successfully')
            return redirect('admin_dashboard')
            
        elif action == 'withdraw':
            if not withdrawal_amount or withdrawal_amount.strip() == '':
                messages.info(request, "Please enter a valid withdrawal amount.")
                return redirect('admin_dashboard')
            
            user=BankAccount.objects.get(username=user_name)
            try:
                withdrawal_amount = Decimal(withdrawal_amount)
            except ValueError:
                messages.info(request,'invalid amount')
            if withdrawal_amount<=0:
                messages.info(request,'invalid amount')
                return redirect('admin_dashboard')
            user.withdraw(withdrawal_amount)
            user.save()
            messages.info(request,'Amount  withdrawed successfully')
            return redirect('admin_dashboard')
            
        elif action == 'view_details':
            # Retrieve details of the selected user
            if not user_name or user_name.strip() == '':
                messages.info(request, "Please select a valid user.")
                return redirect('admin_dashboard')
            selected_user = BankAccount.objects.get(username=user_name)
            
            all_users = BankAccount.objects.all()
            # Render a template with details or redirect to a details view
            return render(request, 'admin_dashboard.html', {'all_users': all_users,'user_details': selected_user})

        elif action == 'delete':
            if not user_name or user_name.strip() == '':
                messages.info(request, "Please select a valid user.")
                return redirect('admin_dashboard')
            selected_user = BankAccount.objects.get(username=user_name)
            selected_user.delete()
            all_users = BankAccount.objects.all()
            return redirect('admin_dashboard')
    
    all_users = BankAccount.objects.all()
    return render(request, 'admin_dashboard.html', {'all_users': all_users})
