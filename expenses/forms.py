from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = ['category', 'title', 'amount', 'date', 'description']

        widgets = {

            'description': forms.Textarea(
                attrs={
                    'rows': 2,
                    'class': 'form-control'
                }
            ),

            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'amount': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),

            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'category': forms.Select(
                attrs={'class': 'form-control'}
            )

        }