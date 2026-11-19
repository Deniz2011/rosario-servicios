from django.contrib import admin
from .models import (
    ServiceRequest,
    Proposal,
    ProviderProfile,
    ProviderService
)


class ProviderServiceInline(admin.TabularInline):
    model = ProviderService
    extra = 1
    fields = (
        "category",
        "service_name",
        "description",
        "price_type",
        "min_price",
        "max_price",
    )


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "experience_years")
    inlines = [ProviderServiceInline]


admin.site.register(ServiceRequest)
admin.site.register(Proposal)