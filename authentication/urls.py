from django.urls import path
from . import views


urlpatterns = [
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
    path('user_create/', views.user_create, name='user_create'),
    path('user_activate/<str:id>/', views.user_activate, name='user_activate'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password_send_email/', views.forgot_password_send_email, name='forgot_password_send_email'),
    path('change_password/<str:id>/', views.change_password, name='change_password'),
    path('change_password_success/', views.change_password_success, name='change_password_success'),
]
