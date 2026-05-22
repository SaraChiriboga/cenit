from django.contrib import admin
from .models import Genero, Artista, Album, Cancion, Colaboracion


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista de géneros [cite: 8]
    list_display = ('idgenero', 'nombregenero', 'descripcion')
    # Permite buscar géneros por nombre o descripción
    search_fields = ('nombregenero', 'descripcion')
    ordering = ('idgenero',)


@admin.register(Artista)
class ArtistaAdmin(admin.ModelAdmin):
    # Despliega la información clave del artista en el listado [cite: 30, 32]
    list_display = ('idartista', 'nombreartistico', 'paisorigen', 'estadoactivo', 'fecharegistro')
    # Filtro lateral por estado (Vigente/Archivado) y país de origen [cite: 30]
    list_filter = ('estadoactivo', 'paisorigen')
    # Buscador por nombre artístico o país
    search_fields = ('nombreartistico', 'paisorigen')
    ordering = ('idartista',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    # Listar álbumes mostrando metadatos y el ID de su artista [cite: 35]
    list_display = ('idalbum', 'tituloalbum', 'fechalanzamiento', 'artista_idartista')
    # Filtrar álbumes por su año o fecha exacta de lanzamiento
    list_filter = ('fechalanzamiento',)
    search_fields = ('tituloalbum',)
    ordering = ('idalbum',)


@admin.register(Cancion)
class CancionAdmin(admin.ModelAdmin):
    # Muestra las canciones con filtros detallados y la URL de Spotify agregada
    list_display = (
        'idcancion',
        'titulocancion',
        'duracion_formateada',
        'esexplicita',
        'estadopublicacion',
        'album_idalbum',
        'spotify_link'
    )
    # Filtro lateral por estado de publicación y si contiene contenido explícito [cite: 39]
    list_filter = ('estadopublicacion', 'esexplicita')
    # Barra de búsqueda para rastrear títulos de canciones [cite: 39]
    search_fields = ('titulocancion', 'spotifyurlapi')
    ordering = ('idcancion',)

    # Campo personalizado para mostrar la duración de forma elegante (MM:SS)
    def duracion_formateada(self, obj):
        if obj.duracionseg:
            minutos = obj.duracionseg // 60
            segundos = obj.duracionseg % 60
            return f"{minutos}:{segundos:02d}"
        return "0:00"
    duracion_formateada.short_description = 'Duración (MM:SS)'

    # Transforma la URL de la API en un enlace cliqueable dentro del Admin de Django
    def spotify_link(self, obj):
        if obj.spotifyurlapi:
            return f'<a href="{obj.spotifyurlapi}" target="_blank">🔗 Ver en Spotify</a>'
        return "No asignada"
    # Permitir renderizado HTML seguro en el panel administrativo
    spotify_link.allow_tags = True
    spotify_link.short_description = 'Spotify API URL'


@admin.register(Colaboracion)
class ColaboracionAdmin(admin.ModelAdmin):
    # Despliega las asignaciones de artistas a canciones con sus respectivos roles [cite: 43, 44]
    list_display = ('idcolaboracion', 'cancion_idcancion', 'artista_idartista', 'rolartista')
    # Filtro por roles de colaboración (ej: Colaborador Principal, Productor, etc.) [cite: 44]
    list_filter = ('rolartista',)
    search_fields = ('rolartista',)
    ordering = ('idcolaboracion',)