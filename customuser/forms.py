from django import forms
from .models import User
from django.utils.translation import gettext as _
from datetime import date
from datetime import datetime
from django.utils import formats
from django.contrib.auth import forms as auth_forms

class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].required = True

    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','password','password2','birth_date','bio','location')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if len(password1) < 8:
            raise forms.ValidationError('Password too short')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_my_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        birth_date = datetime.strptime(birth_date, '%m/%d/%Y')
        if birth_date >= datetime.now():
            raise forms.ValidationError(u'Wrong Date!')
        return birth_date

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LogInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
    class Meta:
        model = User
        fields = ('email', 'password')
    def clean_password(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError('Password too short')
        return password

class UserVerifyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        userpk = kwargs.pop('pk')
        super(UserVerifyForm, self).__init__(*args, **kwargs)
        self.fields['uid'].initial = userpk
    #self.instance.first == self.cleaned_data.get("user")
    uid = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = User
        fields = ('uid',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class CustomUserProfileForm(forms.ModelForm):
    def __init__(self,user,*args, **kwargs):
        super(CustomUserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['birth_date'].initial = formats.date_format(user.birth_date, "Y-m-d")
        self.fields['bio'].initial = user.bio
        self.fields['location'].initial = user.location
        self.fields['avatar'].initial = user.avatar
    class Meta:
        model = User
        #fields = ('__all__')
        fields = ('first_name','last_name','birth_date','bio','location','avatar')#,'email'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_my_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        birth_date = datetime.strptime(birth_date, '%m/%d/%Y')
        if birth_date >= datetime.now():
            raise forms.ValidationError(u'Wrong Date!')
        return birth_date

class CustomUserPasswordForm(forms.ModelForm):

    uid = forms.IntegerField(widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def __init__(self,user,*args, **kwargs):
        super(CustomUserPasswordForm, self).__init__(*args, **kwargs)
        self.fields['uid'].initial = user.id
    class Meta:
        model = User
        fields = ('uid','password','password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if len(password1) < 8:
            raise forms.ValidationError('Password too short')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
