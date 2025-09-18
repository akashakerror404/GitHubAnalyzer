from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch-user/', views.fetch_user_data, name='fetch_user_data'),
    path('fetch-from-db/', views.fetch_from_db, name='fetch_from_db'),
]