from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class CreateUserForm(UserCreationForm):# UserCreatetionFrom is djangomodel 
    class Meta:
        model= User
        fields=['username','email','password1','password2']



from django import forms
from .models import BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['username', 'account_number', 'balance']

    # def clean(self):
    #     cleaned_data = super().clean()
    #     deposit_amount = cleaned_data.get('deposit_amount')
    #     withdraw_amount = cleaned_data.get('withdraw_amount')

    #     if deposit_amount and withdraw_amount:
    #         raise forms.ValidationError('Cannot deposit and withdraw at the same time. Choose one.')

    #     if not deposit_amount and not withdraw_amount:
    #         raise forms.ValidationError('Please enter deposit or withdraw amount.')

    #     return cleaned_data
    