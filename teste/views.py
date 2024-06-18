from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from pathlib import Path
import os
import pathlib
from Users.models import Profile
from .models import foo 
from forms import PerfilForm
from random import shuffle
from django.db.models import Q
from django.http import Http404

BASE_DIR = Path(__file__).parent.parent

home_ = os.path.join(BASE_DIR/"base_templates"/"global"/"index.html")
detail_ = os.path.join(BASE_DIR/"base_templates"/"global"/"detail.html")
# Create your views here.
results_ = os.path.join(BASE_DIR/"base_templates"/"global"/"results.html")

def home(request):
    profiles = Profile.objects.filter(
        photo__isnull=False,
        cargo__isnull=False,
        first_name__isnull=False,
        description__isnull=False
    )
    
    foos = foo.objects.filter(
        photo__isnull=False,
        cargo__isnull=False,
        first_name__isnull=False,
        description__isnull=False
    )

    perfis = list(profiles) + list(foos)
    shuffle(perfis)

    # Filtrar os perfis que têm os campos cargo, first_name e description preenchidos
    perfis_filtrados = [perfil for perfil in perfis if perfil.cargo and perfil.first_name and perfil.description]

    paginator = Paginator(perfis_filtrados, 6)  # Paginação com 6 perfis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'perfis': perfis_filtrados,
    }
    return render(request, home_, context)

def detail(request, id):
    try:
        usuario = get_object_or_404(foo, id=id)
    # Se o objeto não for encontrado no modelo foo, tente no modelo Profile
    except Http404:
        usuario = get_object_or_404(Profile, id=id)

    context = {
        "usuario": usuario
    }
    return render(request, detail_, context)

def search_profiles(request):
    search_query = request.GET.get('search', '').strip()
    usuarios = foo.objects.filter(
        photo__isnull=False,
        cargo__isnull=False,
        first_name__isnull=False,
        description__isnull=False)
    
    if search_query:
        usuarios = usuarios.filter(
            Q(first_name__icontains=search_query) | 
            Q(cargo__icontains=search_query)
        )
    else:
        pass

    paginator = Paginator(usuarios, 6)  # Paginação com 6 perfis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, results_, {'usuarios': usuarios, 'search_profiles': search_query, 'page_obj': page_obj})

def criar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)
        if form.is_valid():
            # Criar uma instância do modelo Perfil e preencher com os dados do formulário
            perfil = foo(
                first_name=form.cleaned_data['nome'],
                last_name=form.cleaned_data['sobrenome'],
                cargo=form.cleaned_data['cargo'],
                age=form.cleaned_data['idade'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['telefone'],
                description=form.cleaned_data['descricao'],
                photo=form.cleaned_data['photo'],)
            
            perfil.save()
            return redirect("home")
    else:
        form = PerfilForm()
    return render(request, home_, {'form': form})