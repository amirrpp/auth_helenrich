from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.http import is_safe_url

from .utils import normalise_email

User = get_user_model()


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_('Email address'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    def __init__(self, host, *args, **kwargs):
        self.host = host
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url


class EmailUserCreationForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email address'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label=_('User name'), widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label=_('Confirm password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    redirect_url = forms.CharField(
        widget=forms.HiddenInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'username')

    def __init__(self, host=None, *args, **kwargs):
        self.host = host
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = normalise_email(self.cleaned_data['email'])
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("A user with that email address already exists"))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def clean_redirect_url(self):
        url = self.cleaned_data['redirect_url'].strip()
        if url and is_safe_url(url, self.host):
            return url
        return settings.LOGIN_REDIRECT_URL

    def save(self, commit=True):
        user = super(EmailUserCreationForm, self).save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class EmailUserChangeForm(EmailUserCreationForm):
    old_password = forms.CharField(label=_('Old password'),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        self.fields['old_password'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_email(self):
        email = normalise_email(self.cleaned_data['email'])
        # user = User._default_manager.filter(email__iexact=email)
        # if user.exists():
        #     raise forms.ValidationError(
        #         _("A user with that email address already exists"))
        return email

    def clean_old_password(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('old_password')
        if password1 or password2:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                if not self.user_cache.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
        return password

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('old_password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                if not self.user_cache.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )

        return self.cleaned_data
