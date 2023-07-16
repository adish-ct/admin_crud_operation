from django.urls import path
from admin_app import views

# app_name = 'admin_app'


urlpatterns = [
    path('', views.admin_log_in, name='admin_log_in'),
    path('dashboard/', views.admin_home, name='admin_home'),
    path('add_user/', views.admin_add_user, name='admin_add_user'),
    path('delete_user/<int:id>/', views.admin_delete_user, name='admin_delete_user'),
    path('update_user/<int:id>/', views.admin_update, name='admin_update'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_search/', views.admin_search, name='admin_search'),
]