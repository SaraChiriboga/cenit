from django.urls import path
from . import views

urlpatterns = [
    # Esta es la ruta raíz de tu app catálogo, que llama a tu vista
    path('', views.catalog_overview, name='catalog_overview'),
]