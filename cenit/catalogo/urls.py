from django.urls import path
from . import views

urlpatterns = [
    # ── Canciones ──
    path('', views.catalog_overview, name='songs_overview'),
    path('canciones/add/', views.add_track_view, name='add_track'),
    path('canciones/sync/<int:cancion_id>/', views.sync_spotify_track, name='sync_spotify_track'),
    path('api/search-spotify/', views.search_spotify_ajax, name='search_spotify_ajax'),
    path('api/check-existence/', views.check_existence, name='check_existence'),

    # ── Artistas ──
    path('artistas/', views.artista_list, name='artists_overview'),
    path('artistas/add/', views.artista_add, name='artista_add'),
    path('artistas/<int:pk>/edit/', views.artista_edit, name='artista_edit'),
    path('artistas/<int:pk>/delete/', views.artista_delete, name='artista_delete'),

    # ── Álbumes ──
    path('albumes/', views.album_list, name='albums_overview'),
    path('albumes/add/', views.album_add, name='album_add'),
    path('albumes/<int:pk>/edit/', views.album_edit, name='album_edit'),
    path('albumes/<int:pk>/delete/', views.album_delete, name='album_delete'),

    # ── Géneros ──
    path('generos/', views.genero_list, name='genre_overview'),
    path('generos/add/', views.genero_add, name='genero_add'),
    path('generos/<int:pk>/edit/', views.genero_edit, name='genero_edit'),
    path('generos/<int:pk>/delete/', views.genero_delete, name='genero_delete'),

    # ── Colaboraciones ──
    path('colaboraciones/', views.colaboracion_list, name='colabs_overview'),
    path('colaboraciones/add/', views.colaboracion_add, name='colaboracion_add'),
    path('colaboraciones/<int:pk>/edit/', views.colaboracion_edit, name='colaboracion_edit'),
    path('colaboraciones/<int:pk>/delete/', views.colaboracion_delete, name='colaboracion_delete'),
]