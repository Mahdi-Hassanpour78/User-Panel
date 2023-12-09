from django.contrib.auth.mixins import UserPassesTestMixin
import requests
import pyotp
from django.utils import timezone
from accounts.models import OtpCode
from datetime import timedelta


class OtpGenerator:
	@staticmethod
	def generate_otp():
		totp = pyotp.TOTP(pyotp.random_base32())
		code = totp.now()
		return code

	@staticmethod
	def send_otp(phone_number, code, action='default'):
#		data = {'bodyId': 524, 'to': phone_number, 'args':[f'{code}']}
#		response = requests.post('your api key ', json=data)
#		print(response.json())
		print(f"Sending OTP code {code} to {phone_number} - {action}")
		OtpCode.objects.filter(phone_number=phone_number).delete()
		OtpCode.objects.create(phone_number=phone_number, code=code, action=action)

	@staticmethod
	def cleanup_expired_code():
		expiration_time = timezone.now() - timedelta(minutes=1)
		OtpCode.objects.filter(created__lt=expiration_time).delete()


class IsAdminUserMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.is_admins