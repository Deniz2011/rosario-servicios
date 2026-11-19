from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify
from django.forms import inlineformset_factory

class ProviderRegistrationForm(forms.Form):

    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    phone_number = forms.CharField(
    max_length=20,
    label="Número de teléfono",
    help_text="Incluye el código de país. Ejemplo: +5493411234567"
)
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña",
        validators=[validate_password]
    )

    def save(self):
        email = self.cleaned_data["email"]
        base_username = slugify(email.split("@")[0]) or "profesional"

        username = f"{base_username}_provider"
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}_provider{counter}"
            counter += 1

        user = User.objects.create_user(
    username=username,
    email=email,
    password=self.cleaned_data["password"],
    first_name=self.cleaned_data["first_name"],
    last_name=self.cleaned_data["last_name"]
)
        UserProfile.objects.create(
            user=user,
            phone_number=self.cleaned_data["phone_number"]
)
        return user
from .models import ProviderProfile, ProviderService, UserProfile


class ProviderProfileForm(forms.ModelForm):
    dni = forms.CharField(
        max_length=30,
        label="DNI",
        required=True
    )
    class Meta:
        model = ProviderProfile
        fields = [
            "experience_years",
            "description",
            "work_zones",
        ]

        labels = {
            "experience_years": "Años de experiencia",
            "description": "Sobre mí",
            "work_zones": "Zonas de trabajo",
        }    
class ProviderServiceForm(forms.ModelForm):
       
    class Meta:
        model = ProviderService
        fields = [
            "category",
            "service_name",
            "description",
            "price_type",
            "min_price",
            "max_price",
        ]        
class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["phone_number"]
        labels = {
            "phone_number": "Número de teléfono"
        }    
ProviderServiceFormSet = inlineformset_factory(
    ProviderProfile,
    ProviderService,
    form=ProviderServiceForm,
    extra=1,
    can_delete=True
)
       