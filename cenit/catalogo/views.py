import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cancion
from .spotify_service import SpotifyClient
from django.db.models import Q


@login_required
def catalog_overview(request):
    # 1. Obtenemos el QuerySet base optimizado con select_related
    canciones_db = Cancion.objects.select_related('album').all()

    # 2. Capturamos el término de búsqueda enviado por el formulario (si existe)
    query = request.GET.get('q', '')

    # 3. Si el usuario escribió algo, aplicamos los filtros
    if query:
        # Limpiamos el prefijo 'TRK-' por si el usuario lo escribe al buscar por ID
        query_id = query.upper().replace('TRK-', '').strip()

        canciones_db = canciones_db.filter(
            Q(titulocancion__icontains=query) |  # Busca en el título de la canción
            Q(album__tituloalbum__icontains=query) |  # Busca en el título del álbum
            Q(idcancion__icontains=query_id)  # Busca en la columna del ID
        )

    # Pasamos los resultados (filtrados o completos) a la plantilla
    context = {
        'canciones': canciones_db
    }

    return render(request, 'catalogo/catalog_overview.html', context)


def sync_spotify_track(request, cancion_id):
    cancion = get_object_or_404(Cancion, idcancion=cancion_id)
    nombre_artista = cancion.album.artista.nombreartistico if cancion.album and cancion.album.artista else ""

    spotify = SpotifyClient()
    spotify_data = spotify.search_track_info(cancion.titulocancion, nombre_artista)

    if spotify_data:
        cancion.spotifyurlapi = spotify_data['spotify_url']
        cancion.urlportada = spotify_data['album_cover_url']
        cancion.save(update_fields=['spotifyurlapi', 'urlportada'])
        messages.success(request, f"'{cancion.titulocancion}' sincronizada.")
    else:
        messages.error(request, f"No se pudo sincronizar '{cancion.titulocancion}'.")

    return redirect('catalog_overview')


@login_required
def search_spotify_ajax(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    spotify = SpotifyClient()
    # Asumimos que el usuario escribe "Título - Artista" o solo el título
    results = spotify.search_track_info(query, "")

    if results:
        return JsonResponse(results)
    return JsonResponse({'error': 'No encontrado'}, status=404)

@login_required
def add_track_view(request):
    # Por ahora, solo renderiza la plantilla.
    # Luego aquí pondremos la lógica del formulario.
    return render(request, 'catalogo/add_track.html')

def search_track_info(self, query):
    if not self.token: return None
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {self.token}"}
    params = {"q": query, "type": "track", "limit": 5}  # Traemos 5 resultados

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        return [
            {
                'id': t['id'],
                'name': t['name'],
                'artist': t['artists'][0]['name'],
                'spotify_url': t['external_urls']['spotify'],
                'album_cover': t['album']['images'][1]['url'] if t['album']['images'] else None,
                'duration': round(t['duration_ms'] / 1000)
            } for t in tracks
        ]
    return []