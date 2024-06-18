from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import os
from pathlib import Path
from .models import Profile
from .forms import LoginForm, DeleteAccountForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileEditForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# Create your views here.

BASE_DIR = Path(__file__).parent.parent
auth_ = os.path.join(BASE_DIR/"base_templates"/"global"/"authentication.html")
register_ = os.path.join(BASE_DIR/"base_templates"/"global"/"register.html")
user_ = os.path.join(BASE_DIR/"base_templates"/"global"/"user.html")
home_ = os.path.join(BASE_DIR/"base_templates"/"global"/"index.html")
delete_ = os.path.join(BASE_DIR/"base_templates"/"global"/"delete.html")
success_ = os.path.join(BASE_DIR/"base_templates"/"global"/"success.html")

def authentication(request):
    print("View authentication foi chamada.")
    request.session['previous_url'] = request.META.get('HTTP_REFERER', '/')

    print("estou morrendo aqui")
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        
        if form.is_valid():
            print("estou no formulário")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user_profile')  # Redirecionar para a página de perfil após o login bem-sucedido
            else:
                form.add_error(None, 'Credenciais inválidas. Por favor, tente novamente.')
                return render(request, home_, {'form': form})  # Renderize novamente a página de autenticação com erros
    else:
        form = LoginForm()  
    return render(request, auth_, {'form': form})  # Renderize a página de autenticação em caso de solicitação GET


def register(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Autenticar o usuário recém-registrado
            user = authenticate(request, username=user.username, password=form.cleaned_data['password'])
            if user:
                login(request, user)

                # Redirecionar para a página de perfil do usuário
                return redirect('user_profile')  # Use o nome da URL reversa definida em urls.py
    else:
        user_form = UserRegistrationForm()
    return render(request, register_, {'form': form})

@login_required
@csrf_protect
def user_profile(request):
    # Inicialize a variável profile_form como None
    profile_form = None

    try:
        # Tente recuperar o perfil associado ao usuário autenticado
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Se o perfil não existe, você pode lidar com isso de acordo com sua lógica
        # Aqui, criamos um perfil em branco como exemplo
        user_profile = Profile(user=request.user)
        user_profile.save()

    if request.method == 'POST':
        # Se o método da solicitação for POST, isso significa que o formulário foi enviado
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            # Se o formulário for válido, salve os dados
            profile_form.save()
            # Redirecione para a mesma página após a atualização bem-sucedida
            return HttpResponseRedirect(request.path_info)
    else:
        # Se a solicitação não for POST, inicialize o formulário com os dados do perfil
        profile_form = ProfileEditForm(instance=user_profile)

    # Passe o formulário ProfileEditForm como parte do contexto
    return render(request, user_, {'user_profile': user_profile, 'profile_form': profile_form})

@login_required
def edit_profile(request):
    print("Estou no edit profile")
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            print("no salvei o formulário")
            return render(request, success_)
    else:
        # Se o método da solicitação não for POST, crie uma instância do formulário ProfileEditForm com os dados existentes
        profile_form = ProfileEditForm(instance=user_profile)
        print("Estou no else")

    # Passe o formulário ProfileEditForm como parte do contexto
    return render(request, user_, {'user_profile': user_profile, 'profile_form': profile_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        # Redirecionar para a página de login ou outra página desejada após a exclusão da conta
    return render(request, delete_, {
        'next': request.META['HTTP_REFERER'],
    })

def logoff(request):
    logout(request)
    return redirect('home')
