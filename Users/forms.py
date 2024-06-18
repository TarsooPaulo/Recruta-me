from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']

        # Verifique se o usuário existe no banco de dados
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este usuário não existe.')
        
        if not self.cleaned_data['username']:
            raise forms.ValidationError('Por favor, digite um nome de usuário.')


        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
        except:
            raise ValidationError('Senha incorreta.')
        # Verifique se a senha corresponde ao usuário
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('Senha incorreta.')

        return password


    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput,
        min_length=8,  # Define o comprimento mínimo da senha
        error_messages={
            'min_length': 'A senha deve ter pelo menos 8 caracteres.'  # Mensagem de erro personalizada
        }
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username',)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        # Verifica se o usuário já existe
        user = User.objects.filter(username=username).first()
        if user is not None:
            # Adiciona o erro personalizado
            self.add_error('username', 'Usuário existente, por favor tente outro')

        # Verifica se o password e confirm_password estão corretos
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")

    def clean_username(self):
        username = self.cleaned_data['username']

        # Verifique se o usuário existe no banco de dados
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário já utilizado')

        return username

    # Adicione o seguinte código para traduzir o campo `username` para `usuário`

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuário'

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        fields = ['first_name', 'last_name', 'email', 'age', 'cargo', 'phone', 'photo', 'description']

    # def __init__(self, *args, **kwargs):
    #     super(ProfileEditForm, self).__init__(*args, **kwargs)
    #     self.fields['description'].widget.attrs['style'] = 'width: 322px; height: 87px;'

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if any(char.isdigit() for char in first_name):
            raise ValidationError('O nome não pode conter números.')
        return first_name

    def save(self, commit=True):
        instance = super(ProfileEditForm, self).save(commit=False)
        instance.first_name = self.cleaned_data['first_name']
        if commit:
            instance.save()
        return instance

class DeleteAccountForm(forms.Form):
    confirm_delete = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Confirme que você deseja deletar sua conta. Esta ação é irreversível.",
    )