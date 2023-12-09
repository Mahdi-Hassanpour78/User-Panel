from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
#from datetime import timedelta


class UserManager(BaseUserManager):
	def create_user(self, phone_number, email=None, name=None, password=None):
		if not phone_number:
			raise ValueError('User must have phone number')

		user = self.model(phone_number=phone_number, email=self.normalize_email(email), name=name)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone_number, email=None, name=None, password=None):
		user = self.create_user(phone_number, email, name, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	phone_number = models.CharField(max_length=11, unique=True)
	email = models.EmailField(blank=True, null=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	national_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
	address = models.TextField()
	is_active = models.BooleanField(default=True)

	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email', 'name']

	def __str__(self):
		return self.phone_number



class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	action = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'

	def is_expired(self):
		expiration_time = timezone.now() - timezone.timedelta(minutes=1)
		return self.created > expiration_time
