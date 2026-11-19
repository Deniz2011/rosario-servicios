

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class ServiceRequest(models.Model):
    name = models.CharField(
    max_length=100,
    blank=True,
    verbose_name="Nombre y apellido" )   
    email = models.EmailField(blank=True,
    verbose_name="Correo electrónico")
    category = models.CharField(max_length=100, blank=True,
    verbose_name="Categoría")
    title = models.CharField(max_length=200,
    verbose_name="Título")
    description = models.TextField(
    verbose_name="Descripción")

    location = models.CharField(max_length=100,
    verbose_name="Barrio")
    address = models.CharField(max_length=200, blank=True,
    verbose_name="Dirección")

    budget = models.IntegerField(null=True, blank=True,
    verbose_name="Presupuesto (ARS)")

    def __str__(self):
        return self.title
    
class Proposal(models.Model):
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="proposals"
    )
    provider_name = models.CharField(max_length=100)
    provider_email = models.EmailField()
    price = models.IntegerField(verbose_name="Precio de la propuesta (ARS)")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
    max_length=20,
    default="pending",
    choices=[
        ("pending", "Pendiente"),
        ("accepted", "Aceptada"),
        ("rejected", "Rechazada"),
    ]
)
    def __str__(self):
        return f"{self.provider_name} - ${self.price}"
    from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de teléfono"
    )
    dni = models.CharField(
    max_length=30,
    unique=True,
    null=True,
    blank=True,
    verbose_name="DNI"
)
    def __str__(self):
        return self.user.username

class ProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )

    experience_years = models.PositiveIntegerField(
        verbose_name="Años de experiencia"
    )

    description = models.TextField(
        verbose_name="Sobre mí"
    )

    work_zones = models.CharField(
        max_length=300,
        verbose_name="Zonas de trabajo"
    )

   

    def __str__(self):
        return self.user.username
class ProviderService(models.Model):

    CATEGORY_CHOICES = [
        ("Limpieza", "Limpieza"),
        ("Electricidad", "Electricidad"),
        ("Plomería", "Plomería"),
        ("Reparaciones", "Reparaciones"),
        ("Pintura", "Pintura"),
        ("Jardinería", "Jardinería"),
        ("Mudanzas", "Mudanzas"),
        ("Otros", "Otros"),
    ]

    PRICE_TYPES = [
        ("fixed", "Precio fijo"),
        ("range", "Rango de precios"),
        ("negotiable", "A convenir"),
    ]

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="services"
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    service_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    price_type = models.CharField(
        max_length=20,
        choices=PRICE_TYPES,
        default="range"
    )

    min_price = models.PositiveIntegerField(null=True, blank=True)
    max_price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_name} - {self.provider.user.username}"