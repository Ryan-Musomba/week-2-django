from django.urls import path
from photoapp import views
from django.contrib.auth import views as auth_views
from photoapp.forms import CustomPasswordResetForm, CustomSetPasswordForm

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_update_view, name='profile_update'),
    path('photo/upload/', views.photo_upload_view, name='photo_upload'),
    path('photo/<int:pk>/', views.photo_detail_view, name='photo_detail'),
    path('photo/<int:pk>/like/', views.photo_like_view, name='photo_like'),
    path('change_password/', views.dashboard_view, name='change_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        form_class=CustomPasswordResetForm,
        email_template_name='accounts/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        form_class=CustomSetPasswordForm
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]