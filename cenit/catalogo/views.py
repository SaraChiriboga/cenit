from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cancion
from .spotify_service import SpotifyClient


@login_required # <--- Obliga a loguearse primero
def catalog_overview(request):
    canciones_db = Cancion.objects.select_related('album').all()
    context = {
        'canciones': canciones_db
    }
    return render(request, 'catalogo/catalog_overview.html', context)


def sync_spotify_track(request, cancion_id):
    """Sincroniza una canción específica con la API de Spotify."""
    cancion = get_object_or_404(Cancion, idcancion=cancion_id)

    # Asumimos que podemos llegar al nombre del artista a través del álbum
    # Ajusta esto si en tu modelo real el artista se obtiene diferente
    nombre_artista = cancion.album.artista.nombreartistico if cancion.album and cancion.album.artista else ""

    spotify = SpotifyClient()
    spotify_data = spotify.search_track_info(cancion.titulocancion, nombre_artista)

    if spotify_data:
        # Actualizamos los campos en la tabla Cancion
        cancion.spotifyurlapi = spotify_data['spotify_url']
        cancion.urlportada = spotify_data['album_cover_url']
        cancion.save()
        messages.success(request, f"'{cancion.titulocancion}' sincronizada con éxito.")
    else:
        messages.error(request, f"No se encontró '{cancion.titulocancion}' en Spotify.")

    # Volvemos a la pantalla principal del catálogo
    return redirect('catalog_overview')