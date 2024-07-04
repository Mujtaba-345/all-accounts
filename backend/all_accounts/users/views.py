from django.shortcuts import render, redirect
from django.views import View
from .models import User
from django.contrib import messages
from utils.common import send_verification_email, encode_token, decode_token, password_reset_email
from django.conf import settings
import jwt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from shop.models import Brand, Shop, Lager
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast


class UserSignUpView(View):

    def get(self, request):
        return render(request, "users/signup.html")

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get("password2")
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "user with this name is already exists.")
        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, "user with this email is already exists.")
        elif password1 != password2:
            messages.error(request, "password does not match")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            token = encode_token(user)
            verification_link = f"{settings.HOST_URL}/users/verify_email/{token}/"
            send_verification_email(user, verification_link)
            messages.success(request,
                             "Congratulations you have signup successfully.please verify your email the proceed to login ")
        return render(request, "users/signup.html")


class VerifyEmailView(View):

    def get(self, request, token):
        try:
            payload = decode_token(token)
            user_id = payload['user_id']
            user_obj = User.objects.get(id=user_id)
            if user_obj.is_email_verified:
                messages.success(request, "Your email has been already verified")
            else:
                user_obj.is_email_verified = True
                user_obj.save()
                messages.success(request, "Your email has been verified")

        except jwt.ExpiredSignatureError:
            messages.error(request, "Token has expired")
        except jwt.InvalidTokenError:
            messages.error(request, "Invalid token")
        return render(request, "users/login.html")


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_email_verified:
                messages.error(request,
                               "Your email is not verified. Please verify your email and then proceed to login.")
                return redirect('login')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "users/login.html")


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user = request.user
        brand_count = Brand.objects.filter(user=user).count()
        shop_count = Shop.objects.filter(brand__user=user).count()
        total_balance = Lager.objects.filter(shop__brand__user=user).aggregate(
            total=Sum(Cast('opening_balance', IntegerField()))
        )['total']

        context = {"brand_count": brand_count, "shop_count": shop_count, "total_balance": total_balance if total_balance else 0}
        return render(request, "users/dashboard.html", context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):

    def get(self, request):
        return render(request, "users/change_password.html")

    def post(self, request):
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect current password.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep the user logged in
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('change_password')

        return render(request, "users/change_password.html")


class PasswordResetView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "users/password_reset.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            token = encode_token(user)
            password_reset_link = f"{settings.HOST_URL}/users/password_reset_confirm/?token={token}"
            password_reset_email(user, password_reset_link)
        else:
            messages.error(request, "user email is not found")
        return render(request, "users/password_reset.html")


class PasswordResetConfirmView(View):
    def get(self, request):
        token = request.GET.get("token")
        return render(request, "users/password_reset_confirm.html", {"token": token})

    def post(self, request):
        token = request.POST['token']
        new_password1 = request.POST['password1']
        new_password2 = request.POST['password2']
        payload = decode_token(token)
        user_id = payload["user_id"]
        user_obj = User.objects.get(id=user_id)
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        else:
            user_obj.set_password(new_password1)
            user_obj.save()
            return render(request, "users/password_reset_complete.html")
        return render(request, "users/password_reset_confirm.html")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, pk):
        user_obj = User.objects.get(id=pk)
        context = {"user_obj": user_obj}
        return render(request, "users/profile.html", context)

    def post(self, request, pk):
        user_obj = User.objects.get(id=pk)
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('profile', pk=user_obj.pk)
