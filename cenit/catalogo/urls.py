from django.urls import path
from . import views

urlpatterns = [
    # ── Canciones ──
    path('', views.songs_overview, name='songs_overview'),
    path('canciones/sync/<int:cancion_id>/', views.sync_spotify_track, name='sync_spotify_track'),
    path('api/search-spotify/', views.search_spotify_ajax, name='search_spotify_ajax'),
    path('api/check-existence/', views.check_existence, name='check_existence'),
    path('canciones/add/', views.add_track_ajax, name='add_track'),
    path('canciones/<int:pk>/edit/', views.edit_track, name='edit_track'),
    path('canciones/<int:pk>/', views.read_track, name='read_track'),
    path('canciones/<int:pk>/delete/', views.delete_track, name='delete_track'),

    # ── Artistas ──
    path('artistas/', views.artists_overview, name='artists_overview'),
    path('artistas/add/', views.add_artist, name='add_artist'),
    path('artistas/<int:pk>/', views.read_artist, name='read_artist'),
    path('artistas/<int:pk>/edit/', views.edit_artist, name='edit_artist'),
    path('artistas/<int:pk>/delete/', views.delete_artist, name='delete_artist'),
    path('artistas/add/', views.add_artist, name='artista_add'),
    path('ajax/search-artist/', views.search_artist_spotify_ajax, name='search_artist_spotify_ajax'),

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