from django.shortcuts import render, redirect
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from .models import Expense
from django.db.models import Sum
from django.shortcuts import get_object_or_404

@login_required
def add_expense(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return redirect('dashboard')

    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

@login_required
def dashboard(request):

    expenses = Expense.objects.filter(user=request.user)

    total_expense = sum(exp.amount for exp in expenses)

    category_summary = (
        Expense.objects
        .filter(user=request.user)
        .values('category__name')
        .annotate(total=Sum('amount'))
    )

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'category_summary': category_summary
    }

    return render(request, 'dashboard.html', context)


@login_required
def delete_expense(request, expense_id):

    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    expense.delete()

    return redirect('dashboard')

@login_required
def edit_expense(request, expense_id):

    expense = get_object_or_404(
        Expense,
        id=expense_id,
        user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form})




def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('add_expense')

    return render(request, 'login.html')