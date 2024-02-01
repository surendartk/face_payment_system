

def main(request):

    if request.method == 'POST':
        # Retrieve form data
        recipient_account_number = request.POST.get('recipient_account_number')

        # Validate if the account number exists
        try:
            recipient_account = BankAccount.objects.get(
                account_number=recipient_account_number)
        except BankAccount.DoesNotExist:
            messages.info(request, "Invalid recipient account number")
            return redirect('main')
        # Retrieve the current user's account
        current_user = request.user
        sender_account = BankAccount.objects.get(username=current_user)

        # Retrieve the amount to be transferred
        try:
            amount = Decimal(request.POST.get('amount'))
        except ValueError:
            messages.info(request, "Invalid amount")
            return redirect('main')
        # Check if the user has enough funds
        if recipient_account.account_number == sender_account.account_number:
            messages.info(request, "sender and receier are same")
            return redirect('main')
        if amount <= sender_account.balance and amount > 0:
            # Perform the transfer
            sender_account.withdraw(amount)
            recipient_account.deposit(amount)

            # Update the sender's and recipient's data in the database
            sender_account.save()
            recipient_account.save()

            # Add transaction details to sender and recipient accounts
            sender_account.add_transaction(
                'Sent', amount, recipient_account.account_number)
            recipient_account.add_transaction(
                'Received', amount, sender_account.account_number)

            # Redirect to the main page with updated data
            return redirect('main')
        else:
            messages.info(request, "insufficient amount or zero amount")
            return redirect('main')

    # If the request is not a POST request, render the main page
    current_user = request.user
    data = BankAccount.objects.get(username=current_user)

    return render(request, 'main.html', {'data': data})