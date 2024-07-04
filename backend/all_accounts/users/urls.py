from django.urls import path
from .views import UserSignUpView, VerifyEmailView, LoginView, DashboardView, ChangePasswordView, \
    PasswordResetView, PasswordResetConfirmView, ProfileView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name='user-signup'),
    path("verify_email/<str:token>/", VerifyEmailView.as_view(), name='verify-email'),
    path("login/", LoginView.as_view(), name='login'),
    path("dashboard/", DashboardView.as_view(), name='dashboard'),
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),
    path('change-password/', ChangePasswordView.as_view(),
         name='change_password'),
    path('password_reset/', PasswordResetView.as_view(), name='password-reset'),
    path("password_reset_confirm/", PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("profile/<int:pk>/", ProfileView.as_view(), name='profile')
]
