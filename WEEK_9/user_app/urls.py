from django.urls import path
from user_app import views


urlpatterns = [
    path('', views.log_in, name="log_in"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('home/', views.home, name="home"),
    path('sign_out/', views.sign_out, name="sign_out"),
]