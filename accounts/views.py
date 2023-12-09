from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, UserProfileForm, UserChangeForm
from utils import OtpGenerator
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            otp_code = OtpGenerator.generate_otp()
            OtpGenerator.send_otp(form.cleaned_data['phone_number'], otp_code, action='register')
            request.session['user_registration_info'] = {
                'phone_number': phone_number,
                'otp_code':otp_code,
            }
            messages.success(request, 'We sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        if not user_session:
            return redirect('accounts:register')

        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code and not code_instance.is_expired():
                User.objects.create_user(user_session['phone_number'],)
                code_instance.delete()
                messages.success(request, 'You registered successfully.', 'success')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'This code is invalid or expired', 'danger')
                return redirect('accounts:verify_code')
        return redirect('accounts:dashboard')


class UserLogoutView(LogoutView):
    template_name = 'home/index.html'


class UserLoginRequestView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login_request.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            otp_code = OtpGenerator.generate_otp()
            OtpGenerator.send_otp(phone_number=phone_number, code=otp_code, action='login')

            request.session['login_phone_number'] = phone_number
            request.session['login_otp_code'] = otp_code

            return redirect('accounts:verify_login_code')

        return render(request, self.template_name, {'form': form})


class VerifyLoginCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_session = request.session
            code_instance = OtpCode.objects.get(phone_number=user_session['login_phone_number'])
            entered_code = form.cleaned_data['code']
            if code_instance.is_expired():

                if entered_code == code_instance.code:
                    user, created = User.objects.get_or_create(phone_number=user_session['login_phone_number'])
                    login(request, user)
                    messages.success(request, 'You logged in successfully', 'info')

                    del request.session['login_phone_number']
                    del request.session['login_otp_code']

                    return redirect('accounts:dashboard')
                else:
                    messages.error(request, 'Invalid code', 'warning')
            else:
                messages.error(request, 'otp is expired', 'warning')

        return render(request, self.template_name, {'form': form})


class UserDashboardView(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        user = request.user
        form = UserChangeForm(instance=user)
        return render(request, self.template_name, {'user':user, 'form':form})


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/user_profile.html'

    def get(self, request):
        form = UserChangeForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile information has been updated.', 'success')
            return redirect('accounts:user_profile')
        return render(request, self.template_name, {'form': form})