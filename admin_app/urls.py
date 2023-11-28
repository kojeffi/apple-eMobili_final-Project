from django.urls import path
from .views import admin, register_admin, user_login, user_logout
from .views import forms_elements, update_user, delete_user

from .views import tables_general
from . import views


urlpatterns = [
    path('admin/', admin, name='admin-url'),
    path('register/', register_admin, name='register_admin-url'),
    path('login/', user_login, name='login_admin-url'),
    path('logout/', user_logout, name='logout_admin-url'),
    path('update-user/<int:id>/', update_user, name='update_user'),
    path('delete-user/<int:id>/', delete_user, name='delete_user'),
    path('forms-elements/', forms_elements, name='forms_elements-url'),
    path('tables-general/', tables_general, name='tables_general-url'),
    path('tables-general/', views.tables_general, name='tables_general'),
    path('admin_app/tables-general/<int:id>/', views.tables_general, name='tables-general'),
    path('contact/', views.contact, name='contact-url'),
]
