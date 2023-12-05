from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('phone_number',)

	def clean_phone_number(self):
		phone_number = self.cleaned_data.get('phone_number')
		if User.objects.filter(phone_number=phone_number).exists():
			raise ValidationError('This phone number is already in use.')
		return phone_number


class UserChangeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email', 'phone_number', 'name', 'national_code', 'address', 'last_login')


class UserRegistrationForm(forms.Form):
	phone_number = forms.CharField(max_length=11)

	def clean_phone_number(self):
		phone_number = self.cleaned_data['phone_number']
		user = User.objects.filter(phone_number=phone_number).exists()
		if user:
			raise ValidationError('This phone number already exists')
		OtpCode.objects.filter(phone_number=phone_number).delete()
		return phone_number


class VerifyCodeForm(forms.Form):
	code = forms.IntegerField()


class UserLoginForm(forms.Form):
	phone_number = forms.CharField()


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['name', 'email', 'national_code', 'address']