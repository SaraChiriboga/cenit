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

    def search_track_info_list(self, query):
        if not self.token:
            return []

        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": query, "type": "track", "limit": 5}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            return []

        tracks = response.json().get('tracks', {}).get('items', [])
        results = []

        for t in tracks:
            # Preview de Deezer usando nombre + artista
            preview = self._get_deezer_preview(
                t['name'],
                t['artists'][0]['name']
            )
            results.append({
                'id': t['id'],
                'name': t['name'],
                'artist': t['artists'][0]['name'],
                'album_cover': t['album']['images'][1]['url'] if t['album']['images'] else None,
                'spotify_url': t['external_urls']['spotify'],
                'duration': round(t['duration_ms'] / 1000),
                'preview_url': preview,  # viene de Deezer
            })

        return results

    def _get_deezer_preview(self, name, artist):
        try:
            url = "https://api.deezer.com/search"
            params = {"q": f"{name} {artist}", "limit": 1}
            r = requests.get(url, params=params, timeout=3)
            data = r.json().get('data', [])
            return data[0]['preview'] if data else None
        except Exception:
            return None