from django.contrib.auth.mixins import UserPassesTestMixin
import requests

def send_otp_code(phone_number, code, action):

	data = {'bodyId': 524, 'to': phone_number, 'args':[f'{code}']}
	response = requests.post('your api key ', json=data)
	print(response.json())
#	print(f"Sending OTP code {code} to {phone_number} - {action}")

class IsAdminUserMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.is_admins