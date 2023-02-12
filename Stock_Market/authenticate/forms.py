from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class EditProfileForm(UserChangeForm):

    password = forms.CharField(
        label="", widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = User
        # excludes private information from User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length=150, widget=forms.TextInput(attrs={
                                 'placeholder': 'Enter First Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'xyz@gmail.com', 'class': 'form-control'}), label='')
    last_name = forms.CharField(label="", max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your Password should contain a mix of Uppercase and Lowercase letters</li><li>Your password must contain at least 8 characters.</li><li>Your Password should contain a special characters like !,@,#,$,%,^,&,*,-,+</li></ul>'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # self.fields['username'].help_text = '<small class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></small>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        # self.fields['password2'].help_text = '<small style="color: white;" class="form-text text-muted"><small>Enter the same password as before, for verification.</small></small>'
