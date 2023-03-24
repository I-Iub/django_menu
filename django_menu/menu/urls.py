from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu, name='menu_core'),
    path('<slug:title>/', views.menu, name='menu_title'),
    path('<slug:title>/<slug:item_path>/', views.menu, name='menu_item'),
]
