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
    register
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
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
    path('register/', register, name='register'),
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
]