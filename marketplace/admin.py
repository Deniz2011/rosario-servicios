from .models import UserProfile
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
admin.site.register(ProviderService)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ("user", "phone_number")

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser