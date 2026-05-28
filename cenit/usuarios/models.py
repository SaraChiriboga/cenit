from django.db import models

class Usuario(models.Model):
    idusuario = models.IntegerField(db_column='idUsuario', primary_key=True)
    nombre = models.CharField(db_column='nombre', max_length=50)  # <-- ¡Corregido aquí!
    apellido = models.CharField(db_column='apellido', max_length=50)
    email = models.CharField(db_column='email', max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'Usuario].[Usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"