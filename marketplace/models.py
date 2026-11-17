

# Create your models here.
from django.db import models


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
    def __str__(self):
        return f"{self.provider_name} - ${self.price}"