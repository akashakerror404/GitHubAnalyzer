from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fetch-user/', views.fetch_user_data, name='fetch_user_data'),
    path('fetch-from-db/', views.fetch_from_db, name='fetch_from_db'),


    path('api/school-demo', views.school_demo_request, name='school_demo_request'),
    path('api/book-demo', views.book_demo_request, name='book_demo_request'),

]