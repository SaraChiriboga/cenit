from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cancion

@login_required # <--- Obliga a loguearse primero
def catalog_overview(request):
    canciones_db = Cancion.objects.select_related('album').all()
    context = {
        'canciones': canciones_db
    }
    return render(request, 'catalogo/catalog_overview.html', context)