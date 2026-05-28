from django.contrib import admin
from .models import TipoSuscripcion, Promocion, Suscripcion, Notificacion, Playlist, PlaylistCancion, EstadisticaDiaria

@admin.register(TipoSuscripcion)
class TipoSuscripcionAdmin(admin.ModelAdmin):
    # Columnas visibles en la lista de planes
    list_display = ('idtipo', 'nombreplan', 'precio', 'moneda', 'duracion')
    # Permite buscar planes escribiendo su nombre
    search_fields = ('nombreplan',)


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    # Columnas visibles para controlar las ofertas
    list_display = ('idpromo', 'descripcion', 'porcentajedesc', 'fechainicio', 'fechaexpira', 'estadoactivo', 'tiposuscripcion')
    # Filtros laterales automáticos por estado y rangos de fechas
    list_filter = ('estadoactivo', 'fechainicio', 'fechaexpira')
    # Buscador por la descripción del descuento
    search_fields = ('descripcion',)


@admin.register(Suscripcion)
class SuscripcionAdmin(admin.ModelAdmin):
    # Muestra los datos clave del contrato del cliente
    list_display = ('idsuscripcion', 'usuario', 'tiposuscripcion', 'fechainicio', 'fechafin', 'estado')
    # Filtros laterales para auditar suscripciones caídas o vigentes
    list_filter = ('estado', 'fechainicio', 'fechafin')
    # Permite buscar directo por el ID de suscripción o navegando al nombre/apellido del usuario relacionado
    search_fields = ('idsuscripcion', 'usuario__nombre', 'usuario__apellido')


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('idnotificacion', 'usuario', 'tiponotif', 'fechaenvio')
    list_filter = ('tiponotif', 'fechaenvio')
    search_fields = ('mensaje', 'usuario__nombre', 'usuario__apellido')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    # Despliega el control de las listas de reproducción del sistema
    list_display = ('idplaylist', 'nombre', 'usuario', 'esprivada', 'espublicada', 'fechacreacion')
    list_filter = ('esprivada', 'espublicada', 'fechacreacion')
    search_fields = ('nombre', 'usuario__nombre', 'usuario__apellido')


@admin.register(PlaylistCancion)
class PlaylistCancionAdmin(admin.ModelAdmin):
    # Tabla intermedia de canciones añadidas
    list_display = ('playlist', 'cancion', 'fechaadicion', 'orden')
    search_fields = ('playlist__nombre', 'cancion__titulocancion')


@admin.register(EstadisticaDiaria)
class EstadisticaDiariaAdmin(admin.ModelAdmin):
    # Panel analítico para ver el rendimiento diario de las canciones
    list_display = ('idestat', 'cancion', 'totalrepros', 'fechareporte')
    list_filter = ('fechareporte',)
    search_fields = ('cancion__titulocancion',)