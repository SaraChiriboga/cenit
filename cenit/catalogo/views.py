import requests
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import Cancion, Artista, Album, Genero, Colaboracion
from .spotify_service import SpotifyClient

ESTADOS_PUBLICACION = ['Borrador', 'Programada', 'Publicada']
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


from django.db import connection  # Asegúrate de importar esto


@login_required
@csrf_exempt
def add_track_ajax(request):
    if request.method == 'GET':
        return render(request, 'catalogo/add_track.html', {
            'albumes': Album.objects.all(),
            'generos': Genero.objects.all(),
        })

    if request.method == 'POST':
        try:
            # Captura todos los datos
            titulo = request.POST.get('titulocancion')
            album_id = request.POST.get('album')
            genero_id = request.POST.get('genero')
            duracion = request.POST.get('duracionseg')
            url_portada = request.POST.get('urlportada')
            es_explicita = request.POST.get('esexplicita') == 'on'
            spotify_url = request.POST.get('spotify_url')

            if not titulo or not album_id:
                return JsonResponse({'status': 'error', 'message': 'Faltan campos obligatorios.'}, status=400)

            if Cancion.objects.filter(titulocancion__iexact=titulo, album_id=album_id).exists():
                return JsonResponse({'status': 'error', 'message': 'La canción ya existe en este álbum.'}, status=400)

            # Inserción asegurando que spotifyUrlAPI se guarde
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO [Catalogo].[Cancion] 
                    (tituloCancion, duracionSeg, esExplicita, estadoPublicacion, urlPortada, Album_idAlbum, Genero_idGenero, spotifyUrlAPI)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [titulo, duracion or 0, 1 if es_explicita else 0, 'Borrador', url_portada, album_id, genero_id,
                      spotify_url])

            return JsonResponse({'status': 'success', 'message': 'Canción guardada correctamente.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

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
    nombre = request.GET.get('nombre', '').strip()

    existe = False
    if tipo == 'album':
        existe = Album.objects.filter(tituloalbum__iexact=nombre).exists()
    elif tipo == 'genero':
        existe = Genero.objects.filter(nombregenero__iexact=nombre).exists()
    elif tipo == 'cancion':  # <--- AÑADE ESTO
        existe = Cancion.objects.filter(titulocancion__iexact=nombre).exists()

    return JsonResponse({'existe': existe})

def delete_track(request, pk):
    if request.method == 'POST':
        cancion = get_object_or_404(Cancion, pk=pk)
        cancion.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def read_track(request, pk):
    cancion = get_object_or_404(
        Cancion.objects.select_related('album__artista', 'genero'),
        idcancion=pk
    )
    return render(request, 'catalogo/read_track.html', {
        'cancion': cancion,
        'albumes': Album.objects.all(),
        'generos': Genero.objects.all(),
        'estados': ['Borrador', 'Programada', 'Publicada'],
    })


@login_required
def edit_track(request, pk):
    # Validamos que la canción exista
    cancion = get_object_or_404(Cancion, idcancion=pk)

    if request.method == 'POST':
        # 1. Capturamos la URL exacta que el frontend determinó al cambiar el select
        url_portada_frontend = request.POST.get('urlportada')

        # 2. Hacemos un ÚNICO update respetando la integridad
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE [Catalogo].[Cancion]
                SET tituloCancion=%s, 
                    duracionSeg=%s, 
                    esExplicita=%s,
                    estadoPublicacion=%s, 
                    Album_idAlbum=%s, 
                    Genero_idGenero=%s,
                    urlPortada=%s
                WHERE idCancion=%s
            """, [
                request.POST.get('titulocancion'),
                request.POST.get('duracionseg'),
                1 if request.POST.get('esexplicita') == 'on' else 0,
                request.POST.get('estadopublicacion'),
                request.POST.get('album'),
                request.POST.get('genero'),
                url_portada_frontend,  # <-- Guardamos la portada correcta
                pk
            ])
            # Nota: Django suele hacer autocommit en sus cursores,
            # pero si ves que no se guarda en SQL Server, descomenta la siguiente línea:
            # connection.commit()

        # 3. Devolvemos el éxito y la URL para que el frontend actualice la vista sin recargar
        return JsonResponse({
            'status': 'success',
            'urlportada': url_portada_frontend
        })

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

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
