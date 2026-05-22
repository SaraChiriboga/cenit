from django.urls import path
from . import views

urlpatterns = [
    # Esta es la ruta raíz de tu app catálogo, que llama a tu vista
    path('', views.catalog_overview, name='catalog_overview'),
    path('sync/<int:cancion_id>/', views.sync_spotify_track, name='sync_spotify_track'),
    path('api/search-spotify/', views.search_spotify_ajax, name='search_spotify_ajax'),
    path('add/', views.add_track_view, name='add_track'),
]