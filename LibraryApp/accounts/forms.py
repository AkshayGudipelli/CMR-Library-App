from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CollegeUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'register-form__input',
            
        })
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'register-form__input',
            
        }),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'register-form__input',
            
        }),
        strip=False,
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')  # removed username
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'register-form__input',
                
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'register-form__input',
                
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@cmrec.ac.in'):
            raise ValidationError('You must register using College Email (ending with @cmrec.ac.in)')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        # Generate username = firstname+lastname (lowercased, no spaces)
        first = self.cleaned_data.get('first_name', '').strip().lower()
        last = self.cleaned_data.get('last_name', '').strip().lower()
        base_username = f"{first}{last}" if first or last else self.cleaned_data['email'].split('@')[0]

        # Handle duplicates (append number if username exists)
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username

        if commit:
            user.save()
        return user
