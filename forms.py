from django import forms

class PerfilForm(forms.Form):
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    cargo = forms.CharField(max_length=100)
    idade = forms.IntegerField()
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    descricao = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField()
