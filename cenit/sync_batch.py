import os
import django
import time

# 1. Inicializar el entorno de Django para poder usar tus modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cenit.settings')
django.setup()

# Importamos el modelo y el servicio que creamos antes
from catalogo.models import Cancion
from catalogo.spotify_service import SpotifyClient


def run_batch_sync():
    print("Iniciando sincronización masiva con Spotify...\n")

    # Filtramos las canciones que NO tienen URL de Spotify asignada
    canciones_pendientes = Cancion.objects.select_related('album').filter(
        spotifyurlapi__isnull=True
    ) | Cancion.objects.select_related('album').filter(
        spotifyurlapi__exact=''
    )

    total = canciones_pendientes.count()

    if total == 0:
        print("✅ Todas las canciones ya están sincronizadas.")
        return

    print(f"Buscando datos para {total} canciones...\n")

    spotify = SpotifyClient()
    if not spotify.token:
        print("❌ Error: No se pudo obtener el token de Spotify. Revisa credentials.json.")
        return

    actualizadas = 0

    for cancion in canciones_pendientes:
        # Obtenemos el artista de forma segura
        nombre_artista = cancion.album.artista.nombreartistico if cancion.album and cancion.album.artista else ""

        print(f"Buscando: {cancion.titulocancion} - {nombre_artista}...", end=" ")

        datos = spotify.search_track_info(cancion.titulocancion, nombre_artista)

        if datos:
            cancion.spotifyurlapi = datos['spotify_url']
            cancion.urlportada = datos['album_cover_url']
            cancion.save(update_fields=['spotifyurlapi', 'urlportada'])
            print("✅ Actualizada!")
            actualizadas += 1
        else:
            print("⚠️ No encontrada.")

        # Pequeña pausa para no saturar la API de Spotify y evitar bloqueos (Rate Limiting)
        time.sleep(0.5)

    print(f"\nProceso terminado. Se actualizaron {actualizadas} de {total} canciones.")


if __name__ == '__main__':
    run_batch_sync()