from django.db import models


# ==========================================
# 1. TABLA: TipoSuscripcion (Planes Maestros)
# ==========================================

class TipoSuscripcion(models.Model):
    idtipo = models.IntegerField(db_column='idTipo', primary_key=True)
    nombreplan = models.CharField(db_column='nombrePlan', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    precio = models.DecimalField(db_column='precio', max_digits=10, decimal_places=2)
    moneda = models.CharField(db_column='moneda', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')
    duracion = models.IntegerField(db_column='duracion')

    class Meta:
        managed = False
        db_table = 'Negocio].[TipoSuscripcion'
        verbose_name = 'Tipo de Suscripción'
        verbose_name_plural = 'Tipos de Suscripción'

    def __str__(self):
        return f"{self.nombreplan} ({self.moneda} {self.precio})"


# ==========================================
# 2. TABLA: Promocion (Descuentos y Ofertas)
# ==========================================

class Promocion(models.Model):
    idpromo = models.IntegerField(db_column='idPromo', primary_key=True)
    descripcion = models.CharField(db_column='descripcion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    porcentajedesc = models.DecimalField(db_column='porcentajeDesc', max_digits=5, decimal_places=2)
    fechainicio = models.DateTimeField(db_column='fechaInicio')
    fechaexpira = models.DateTimeField(db_column='fechaExpira', blank=True, null=True)
    estadoactivo = models.BooleanField(db_column='estadoActivo')
    # Relación con TipoSuscripcion
    tiposuscripcion = models.ForeignKey(TipoSuscripcion, on_delete=models.DO_NOTHING,
                                        db_column='TipoSuscripcion_idTipo')

    class Meta:
        managed = False
        db_table = 'Negocio].[Promocion'
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'

    def __str__(self):
        return self.descripcion


# ==========================================
# 3. TABLA: Suscripcion (Contratos de Clientes)
# ==========================================

class Suscripcion(models.Model):
    # Declaramos idSuscripcion como PK para cumplir con Django
    idsuscripcion = models.IntegerField(db_column='idSuscripcion', primary_key=True)
    fechainicio = models.DateTimeField(db_column='fechaInicio')
    fechafin = models.DateTimeField(db_column='fechaFin')
    estado = models.CharField(db_column='estado', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')

    # Llaves Foráneas cruzadas con módulo de Usuarios y tus propias tablas
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='Usuario_idUsuario',
                                blank=True, null=True)
    tiposuscripcion = models.ForeignKey(TipoSuscripcion, on_delete=models.DO_NOTHING,
                                        db_column='TipoSuscripcion_idTipo')
    promocion = models.ForeignKey(Promocion, on_delete=models.DO_NOTHING, db_column='Promocion_idPromo', blank=True,
                                  null=True)

    class Meta:
        managed = False
        db_table = 'Negocio].[Suscripcion'
        verbose_name = 'Suscripción'
        verbose_name_plural = 'Suscripciones'

    def __str__(self):
        return f"Suscripción {self.idsuscripcion} - Estado: {self.estado}"


# ==========================================
# 4. TABLA: Notificacion (Historial de Alertas)
# ==========================================

class Notificacion(models.Model):
    idnotificacion = models.IntegerField(db_column='idNotificacion', primary_key=True)
    tiponotif = models.CharField(db_column='tipoNotif', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    mensaje = models.TextField(db_column='mensaje', db_collation='SQL_Latin1_General_CP1_CI_AS')
    fechaenvio = models.DateTimeField(db_column='fechaEnvio')

    # Llaves Foráneas
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='Usuario_idUsuario')
    promocion = models.ForeignKey(Promocion, on_delete=models.DO_NOTHING, db_column='Promocion_idPromo')

    class Meta:
        managed = False
        db_table = 'Auditoria].[Notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f"Notificación {self.idnotificacion} ({self.tiponotif})"


# ==========================================
# 5. TABLA: Playlist (Listas de los Usuarios)
# ==========================================

class Playlist(models.Model):
    idplaylist = models.IntegerField(db_column='idPlaylist', primary_key=True)
    nombre = models.CharField(db_column='nombre', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    descripcion = models.CharField(db_column='descripcion', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS',
                                   blank=True, null=True)
    esprivada = models.BooleanField(db_column='esPrivada')
    espublicada = models.BooleanField(db_column='esPublicada')
    imagenportada = models.CharField(db_column='imagenPortada', max_length=65535,
                                     db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='fechaCreacion')

    # Lliva foránea al creador de la lista
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.DO_NOTHING, db_column='Usuario_idUsuario',
                                blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario].[Playlist'
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.nombre


# ==========================================
# 6. TABLA: PlaylistCancion (Intermedia)
# ==========================================

class PlaylistCancion(models.Model):
    # Nota: Dado que esta tabla usa una PK compuesta en SQL Server y Django exige un campo primary_key,
    # marcamos la playlist como primary_key ya que 'managed=False' evitará que Django altere la BD real.
    playlist = models.ForeignKey(Playlist, on_delete=models.DO_NOTHING, db_column='Playlist_idPlaylist',
                                 primary_key=True)
    cancion = models.ForeignKey('catalogo.Cancion', on_delete=models.DO_NOTHING, db_column='Cancion_idCancion')
    fechaadicion = models.DateTimeField(db_column='fechaAdicion')
    orden = models.IntegerField(db_column='orden')

    class Meta:
        managed = False
        db_table = 'Usuario].[PlaylistCancion'
        unique_together = (('playlist', 'cancion'),)
        verbose_name = 'Canción de Playlist'
        verbose_name_plural = 'Canciones de Playlists'


# ==========================================
# 7. TABLA: EstadisticaDiaria (Analítica)
# ==========================================

class EstadisticaDiaria(models.Model):
    idestat = models.IntegerField(db_column='idEstat', primary_key=True)
    totalrepros = models.IntegerField(db_column='totalRepros')
    fechareporte = models.DateField(db_column='fechaReporte')

    # Llave foránea conectada al catálogo maestro
    cancion = models.ForeignKey('catalogo.Cancion', on_delete=models.DO_NOTHING, db_column='Cancion_idCancion')

    class Meta:
        managed = False
        db_table = 'Auditoria].[EstadisticaDiaria'
        verbose_name = 'Estadística Diaria'
        verbose_name_plural = 'Estadísticas Diarias'

    def __str__(self):
        return f"Estadística {self.idestat} - Fecha: {self.fechareporte}"