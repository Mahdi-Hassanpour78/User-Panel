from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code, action):
    print(f"Sending OTP code {code} to {phone_number} - {action}")


class IsAdminUserMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_authenticated and self.request.user.is_admin
