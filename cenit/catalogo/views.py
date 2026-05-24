import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Cancion, Artista, Album, Genero, Colaboracion
from .spotify_service import SpotifyClient


# ══════════════════════════════════════════
#  CANCIONES
# ══════════════════════════════════════════

@login_required
def catalog_overview(request):
    canciones_db = Cancion.objects.select_related('album').all()
    query = request.GET.get('q', '')
    if query:
        query_id = query.upper().replace('TRK-', '').strip()
        canciones_db = canciones_db.filter(
            Q(titulocancion__icontains=query) |
            Q(album__tituloalbum__icontains=query) |
            Q(idcancion__icontains=query_id)
        )
    return render(request, 'catalogo/songs_overview.html', {'canciones': canciones_db})


@login_required
def add_track_view(request):
    albumes = Album.objects.all()
    generos = Genero.objects.all()
    return render(request, 'catalogo/add_track.html', {
        'albumes': albumes,
        'generos': generos,
    })


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
    return redirect('songs_overview')


@login_required
def search_spotify_ajax(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)
    spotify = SpotifyClient()
    results = spotify.search_track_info_list(query)
    if results:
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'No encontrado'}, status=404)


def check_existence(request):
    tipo = request.GET.get('tipo')
    nombre = request.GET.get('nombre', '').strip()  # Limpia espacios al inicio/final

    existe = False
    if tipo == 'album':
        # Buscamos ignorando mayúsculas y espacios extra
        existe = Album.objects.filter(tituloalbum__iexact=nombre).exists()
    elif tipo == 'genero':
        existe = Genero.objects.filter(nombregenero__iexact=nombre).exists()

    return JsonResponse({'existe': existe})

# ══════════════════════════════════════════
#  ARTISTAS
# ══════════════════════════════════════════

@login_required
def artista_list(request):
    artistas = Artista.objects.all()
    query = request.GET.get('q', '')
    if query:
        artistas = artistas.filter(
            Q(nombreartistico__icontains=query) | Q(paisorigen__icontains=query)
        )
    return render(request, 'catalogo/artists_overview.html', {'artistas': artistas, 'query': query})


@login_required
def artista_add(request):
    # TODO: implementar lógica de guardado
    return render(request, 'catalogo/artista_form.html', {'action': 'Agregar', 'artista': None})


@login_required
def artista_edit(request, pk):
    artista = get_object_or_404(Artista, idartista=pk)
    return render(request, 'catalogo/artista_form.html', {'action': 'Editar', 'artista': artista})


@login_required
def artista_delete(request, pk):
    artista = get_object_or_404(Artista, idartista=pk)
    if request.method == 'POST':
        messages.success(request, f"Artista '{artista.nombreartistico}' eliminado.")
        return redirect('artista_list')
    return render(request, 'catalogo/confirm_delete.html', {'objeto': artista, 'tipo': 'artista'})


# ══════════════════════════════════════════
#  ÁLBUMES
# ══════════════════════════════════════════

@login_required
def album_list(request):
    albumes = Album.objects.select_related('artista').all()
    query = request.GET.get('q', '')
    if query:
        albumes = albumes.filter(
            Q(tituloalbum__icontains=query) | Q(artista__nombreartistico__icontains=query)
        )
    return render(request, 'catalogo/albums_overview.html', {'albumes': albumes, 'query': query})


@login_required
def album_add(request):
    artistas = Artista.objects.all()
    return render(request, 'catalogo/album_form.html', {'action': 'Agregar', 'album': None, 'artistas': artistas})


@login_required
def album_edit(request, pk):
    album = get_object_or_404(Album, idalbum=pk)
    artistas = Artista.objects.all()
    return render(request, 'catalogo/album_form.html', {'action': 'Editar', 'album': album, 'artistas': artistas})


@login_required
def album_delete(request, pk):
    album = get_object_or_404(Album, idalbum=pk)
    if request.method == 'POST':
        messages.success(request, f"Álbum '{album.tituloalbum}' eliminado.")
        return redirect('album_list')
    return render(request, 'catalogo/confirm_delete.html', {'objeto': album, 'tipo': 'álbum'})


# ══════════════════════════════════════════
#  GÉNEROS
# ══════════════════════════════════════════

@login_required
def genero_list(request):
    generos = Genero.objects.all()
    query = request.GET.get('q', '')
    if query:
        generos = generos.filter(nombregenero__icontains=query)
    return render(request, 'catalogo/genre_overview.html', {'generos': generos, 'query': query})


@login_required
def genero_add(request):
    return render(request, 'catalogo/genero_form.html', {'action': 'Agregar', 'genero': None})


@login_required
def genero_edit(request, pk):
    genero = get_object_or_404(Genero, idgenero=pk)
    return render(request, 'catalogo/genero_form.html', {'action': 'Editar', 'genero': genero})


@login_required
def genero_delete(request, pk):
    genero = get_object_or_404(Genero, idgenero=pk)
    if request.method == 'POST':
        messages.success(request, f"Género '{genero.nombregenero}' eliminado.")
        return redirect('genero_list')
    return render(request, 'catalogo/confirm_delete.html', {'objeto': genero, 'tipo': 'género'})


# ══════════════════════════════════════════
#  COLABORACIONES
# ══════════════════════════════════════════

@login_required
def colaboracion_list(request):
    colaboraciones = Colaboracion.objects.select_related('cancion', 'artista').all()
    query = request.GET.get('q', '')
    if query:
        colaboraciones = colaboraciones.filter(
            Q(artista__nombreartistico__icontains=query) | Q(cancion__titulocancion__icontains=query)
        )
    return render(request, 'catalogo/colabs_overview.html', {'colaboraciones': colaboraciones, 'query': query})


@login_required
def colaboracion_add(request):
    canciones = Cancion.objects.all()
    artistas = Artista.objects.all()
    return render(request, 'catalogo/colaboracion_form.html', {
        'action': 'Agregar', 'colaboracion': None,
        'canciones': canciones, 'artistas': artistas,
    })


@login_required
def colaboracion_edit(request, pk):
    colaboracion = get_object_or_404(Colaboracion, idcolaboracion=pk)
    canciones = Cancion.objects.all()
    artistas = Artista.objects.all()
    return render(request, 'catalogo/colaboracion_form.html', {
        'action': 'Editar', 'colaboracion': colaboracion,
        'canciones': canciones, 'artistas': artistas,
    })


@login_required
def colaboracion_delete(request, pk):
    colaboracion = get_object_or_404(Colaboracion, idcolaboracion=pk)
    if request.method == 'POST':
        messages.success(request, "Colaboración eliminada.")
        return redirect('colaboracion_list')
    return render(request, 'catalogo/confirm_delete.html', {'objeto': colaboracion, 'tipo': 'colaboración'})