from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
	path('login/', views.UserLoginRequestView.as_view(), name='login_request'),
    path('verify-login-code/', views.VerifyLoginCodeView.as_view(), name='verify_login_code'),
	path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    path('user_profile/', views.UserProfileView.as_view(), name='user_profile'),
]