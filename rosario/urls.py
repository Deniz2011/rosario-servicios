"""
URL configuration for rosario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from marketplace.views import (
    home,
    need_service,
    offer_service,
    cleaning_profile,
    repair_profile,
    requests_list,
    request_detail,
    proposal,
    proposal_sent,
    send_proposal,
    accept_proposal,
    my_proposals,
    register_provider,
    complete_provider_profile,
    add_provider_service,
    my_provider_services,
    edit_provider_service,
    delete_provider_service,
    my_provider_profile,
    edit_provider_profile,
    profile_updated,
    edit_phone_number,
    phone_updated,
)
urlpatterns = [
    path('admin/', admin.site.urls),
   path('', home, name='home'),
    path('need-service/', need_service),
    path('offer-service/', offer_service),
    path('cleaning-profile/', cleaning_profile),
    path('repair-profile/', repair_profile),
    path('requests/', requests_list),
    path('request/<int:request_id>/', request_detail, name='request_detail'),
    path('request/<int:request_id>/proposal/', send_proposal, name='send_proposal'),
    path('proposal/', proposal),
    path('proposal-sent/', proposal_sent, name='proposal_sent'),
    path('new-request/', proposal),
    path(
    'proposal/<int:proposal_id>/accept/',
    accept_proposal,
    name='accept_proposal'
),
    path('my-proposals/', my_proposals, name='my_proposals'),
    path('register/provider/', register_provider, name='register_provider'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login'
    ),
        path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'provider/complete-profile/',
        complete_provider_profile,
        name='complete_provider_profile'
    ),
    path(
    'provider/add-service/',
    add_provider_service,
    name='add_provider_service'
),
    path(
    'provider/my-services/',
    my_provider_services,
    name='my_provider_services'
),
    path(
    'provider/edit-service/<int:service_id>/',
    edit_provider_service,
    name='edit_provider_service'
),
    path(
    'provider/delete-service/<int:service_id>/',
    delete_provider_service,
    name='delete_provider_service'
),
    path(
    'provider/my-profile/',
    my_provider_profile,
    name='my_provider_profile'
),
    path(
    'provider/edit-profile/',
    edit_provider_profile,
    name='edit_provider_profile'
),
    path(
    'provider/profile-updated/',
    profile_updated,
    name='profile_updated'
),
    path("provider/edit-phone/", edit_phone_number, name="edit_phone_number"),

    path("provider/phone-updated/", phone_updated, name="phone_updated"),
]