import base64
import requests
from django.conf import settings


class SpotifyClient:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.token = self._get_access_token()

    def _get_access_token(self):
        """Pide un token de acceso temporal a Spotify usando tus credenciales."""
        if not self.client_id or not self.client_secret:
            print("Error: Faltan credenciales de Spotify en settings.py")
            return None

        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return response.json()['access_token']
        return None

    def search_track_info(self, track_name, artist_name):
        """Busca una canción y extrae la URL de Spotify y la URL de la portada."""
        if not self.token:
            return None

        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}

        # Combinamos título y artista para que la búsqueda sea exacta
        query = f"track:{track_name} artist:{artist_name}"
        params = {"q": query, "type": "track", "limit": 1}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            items = data.get('tracks', {}).get('items', [])

            if items:
                track = items[0]
                # Retornamos un diccionario con los datos limpios
                return {
                    'spotify_url': track['external_urls']['spotify'],
                    # Tomamos la imagen de tamaño mediano (índice 1) si existe
                    'album_cover_url': track['album']['images'][1]['url'] if track['album']['images'] else None
                }
        return None