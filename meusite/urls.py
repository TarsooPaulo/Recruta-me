"""
URL configuration for meusite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from teste import views as t_views
from Users import views as u_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


# HTTP Request <-> HTTP Response
#Model view Template (MVT)

urlpatterns = [
    path('detalhes/<int:id>/', t_views.detail, name='detail'),
    path('editar_perfil/', u_views.edit_profile, name='edit_profile'),
    path('perfil/', u_views.user_profile, name='user_profile'),
    path('criar_perfil/', t_views.criar_perfil, name='criar_perfil'),
    path('busca/', t_views.search_profiles, name='search_profiles'),
    path('autenticacao/', u_views.authentication, name='authentication'),
    path('deletar_conta/', u_views.delete_account, name='delete_account'),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', u_views.register, name='register'),
    path('Sair/', u_views.logoff, name='logoff'),
    path('admin/', admin.site.urls),
    path('', t_views.home, name="home"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)