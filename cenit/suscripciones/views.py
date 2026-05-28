from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required


@login_required
def usuarios_en_riesgo_view(request):
    usuarios_riesgo = []

    # Consulta SQL nativa para detectar usuarios Premium sin actividad en 30 días
    query = """
            SELECT u.idUsuario, \
                   u.nombre, \
                   u.apellido, \
                   u.email, \
                   s.fechaFin                                 AS fin_suscripcion, \
                   DATEDIFF(day, MAX(r.fechaHora), GETDATE()) AS dias_inactivo
            FROM [Usuario].[Usuario] u
                INNER JOIN [Negocio].[Suscripcion] s \
            ON u.idUsuario = s.Usuario_idUsuario
                LEFT JOIN [Auditoria].[RegistroReproduccion] r ON u.idUsuario = r.Usuario_idUsuario
            WHERE s.estadoSuscripcion = 'Activa'
              AND s.Plan_idPlan = 2 -- Suponiendo que el ID 2 es el plan Premium
            GROUP BY u.idUsuario, u.nombre, u.apellido, u.email, s.fechaFin
            HAVING MAX (r.fechaHora) IS NULL
                OR DATEDIFF(day \
                 , MAX (r.fechaHora) \
                 , GETDATE()) \
                 > 30
            ORDER BY dias_inactivo DESC; \
            """

    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        # Mapeamos los resultados a diccionarios para leerlos fácil en el HTML
        usuarios_riesgo = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'suscripciones/usuarios_riesgo.html', {'usuarios': usuarios_riesgo})