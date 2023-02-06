from django import forms


class InputForm(forms.Form):
    # name = forms.CharField(max_length=200)
    username = forms.EmailField(label='username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=100)
    confirmPassword = forms.CharField(widget=forms.PasswordInput())
