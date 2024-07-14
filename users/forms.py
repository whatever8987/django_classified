from django import forms
from .models import AddCredit
from django.contrib.auth.models import User



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class AddCreditForm(forms.ModelForm):
    class Meta:
        model = AddCredit
        fields = ['amount']  # Only include the amount field since user and timestamp are handled automatically

        # Optional: Add widgets for styling
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
        }
