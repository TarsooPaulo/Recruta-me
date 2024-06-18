from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileEditForm
# Create your tests here.

class ProfileEditFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('teste', 'teste@example.com', 'senha')
        self.profile = Profile.objects.create(user=self.user)

    def test_preencher_formulario(self):
        form = ProfileEditForm(initial={'pk': self.user.pk})

        self.assertEqual(form.cleaned_data['user'], self.user)

        for field in form.fields:
            if field.name in self.profile._meta.get_fields():
                self.assertEqual(form.cleaned_data[field.name], getattr(self.profile, field.name))
