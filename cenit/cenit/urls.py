from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from catalogo import views as catalogo_views # Importas tus vistas

urlpatterns = [
    # Ruta raíz del sitio web: apunta directo a tu vista de catálogo
    path('', catalogo_views.catalog_overview, name='catalog_overview'),
    
    # Rutas del módulo de catálogo (para los detalles, altas, bajas)
    path('catalogo/', include('catalogo.urls')),
    
    # Rutas de autenticación nativas de Django (pero usando tus plantillas)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # El cuarto de máquinas oculto solo para ti si lo necesitas en desarrollo
    path('admin/', admin.site.urls),
]