# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)

# tabla Cancion
class Cancion(models.Model):
    idcancion = models.IntegerField(db_column='idCancion')  # Field name made lowercase.
    titulocancion = models.CharField(db_column='tituloCancion', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    duracionseg = models.IntegerField(db_column='duracionSeg')  # Field name made lowercase.
    esexplicita = models.BooleanField(db_column='esExplicita')  # Field name made lowercase.
    estadopublicacion = models.CharField(db_column='estadoPublicacion', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    album_idalbum = models.IntegerField(db_column='Album_idAlbum')  # Field name made lowercase.
    genero_idgenero = models.IntegerField(db_column='Genero_idGenero')  # Field name made lowercase.
    idcancion_nuevo = models.IntegerField(db_column='idCancion_Nuevo')  # Field name made lowercase.
    spotifyurlapi = models.CharField(db_column='spotifyUrlAPI', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cancion'
        verbose_name = 'Canción'
        verbose_name_plural = 'Canciones'

# tabla Genero
class Genero(models.Model):
    idgenero = models.IntegerField(db_column='idGenero')  # Field name made lowercase.
    nombregenero = models.CharField(db_column='nombreGenero', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    descripcion = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'Genero'
        verbose_name = 'Genero'
        verbose_name_plural = 'Géneros'

# tabla Artista
class Artista(models.Model):
    idartista = models.IntegerField(db_column='idArtista')  # Field name made lowercase.
    nombreartistico = models.CharField(db_column='nombreArtistico', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    biografia = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')  # This field type is a guess.
    paisorigen = models.CharField(db_column='paisOrigen', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    estadoactivo = models.CharField(db_column='estadoActivo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fecharegistro = models.DateTimeField(db_column='fechaRegistro')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Artista'
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

# tabla Album
class Album(models.Model):
    idalbum = models.IntegerField(db_column='idAlbum')  # Field name made lowercase.
    tituloalbum = models.CharField(db_column='tituloAlbum', max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    fechalanzamiento = models.DateField(db_column='fechaLanzamiento')  # Field name made lowercase.
    urlportada = models.CharField(db_column='urlPortada', max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    artista_idartista = models.IntegerField(db_column='Artista_idArtista')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Album'
        verbose_name = 'Álbum'
        verbose_name_plural = 'Álbumes'

# tabla Colaboracion
class Colaboracion(models.Model):
    idcolaboracion = models.IntegerField(db_column='idColaboracion')  # Field name made lowercase.
    rolartista = models.CharField(db_column='rolArtista', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    cancion_idcancion = models.IntegerField(db_column='Cancion_idCancion')  # Field name made lowercase.
    artista_idartista = models.IntegerField(db_column='Artista_idArtista')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Colaboracion'
        verbose_name = 'Colaboración'
        verbose_name_plural = 'Colaboraciones'