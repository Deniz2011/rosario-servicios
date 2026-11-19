from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db import transaction
from django.contrib import messages
from .forms import (
    ProviderRegistrationForm,
    ProviderProfileForm,
    ProviderServiceForm,
    ProviderServiceFormSet,
    UserProfileForm,
)

from .models import (
    ProviderProfile,
    ProviderService,
    UserProfile,
    ServiceRequest,
    Proposal,
)
from .models import ProviderProfile, ProviderService, UserProfile
from django.http import HttpResponse
from .models import ServiceRequest, Proposal


def home(request):
    return render(request, 'index.html')

def need_service(request):
    return render(request, 'hizmet-ariyorum.html')
    
def offer_service(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "provider_profile"):
            return redirect("my_provider_services")
        return redirect("complete_provider_profile")

    return redirect("register_provider")
def cleaning_profile(request):
    return render(request, 'perfil-limpieza.html')

def repair_profile(request):
    return render(request, 'perfil-reparaciones.html')

def requests_list(request):
    requests = ServiceRequest.objects.all()
    return render(request, 'solicitudes.html', {'requests': requests})

def request_detail(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    proposals = service_request.proposals.order_by('-created_at')

    return render(
        request,
        'request-detail.html',
        {
            'service_request': service_request,
            'proposals': proposals
        }
    )
   
def proposal(request):

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        address = request.POST.get("address")
        budget = request.POST.get("budget")

        ServiceRequest.objects.create(
            name=name,
            email=email,
            category=category,
            title=title,
            description=description,
            location=location,
            address=address,
            budget=budget,
        )

        return redirect("proposal_sent")

    return render(request, "propuesta.html")

    return render(request, 'propuesta.html')


def proposal_sent(request):
    return render(request, 'propuesta-enviada.html')


def send_proposal(request, request_id):
    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    if request.method == "POST":
        provider_name = request.POST.get("provider_name")
        provider_email = request.POST.get("provider_email")
        price = request.POST.get("price")
        message = request.POST.get("message")

        Proposal.objects.create(
            service_request=service_request,
            provider_name=provider_name,
            provider_email=provider_email,
            price=price,
            message=message
        )

        return redirect(
            "request_detail",
            request_id=request_id
        )

    return render(
        request,
        'send-proposal.html',
        {'service_request': service_request}
    )
def accept_proposal(request, proposal_id):
    if request.method == "POST":
        proposal = get_object_or_404(
            Proposal,
            id=proposal_id
        )

        Proposal.objects.filter(
            service_request=proposal.service_request
        ).update(status="rejected")

        proposal.status = "accepted"
        proposal.save()

        return redirect(
            "request_detail",
            request_id=proposal.service_request.id
        )

    return redirect("requests_list")
def my_proposals(request):
    proposals = Proposal.objects.order_by('-created_at')

    return render(
        request,
        'my-proposals.html',
        {'proposals': proposals}
    )
def register_provider(request):
    if request.method == "POST":
        form = ProviderRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("complete_provider_profile")
    else:
        form = ProviderRegistrationForm()

    return render(
        request,
        "register-provider.html",
        {"form": form}
    )
@login_required
def complete_provider_profile(request):
    if hasattr(request.user, "provider_profile"):
        return redirect("home")

    user_profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    profile = ProviderProfile(user=request.user)
    service_formset = ProviderServiceFormSet(instance=profile)

    if request.method == "POST":
        form = ProviderProfileForm(request.POST)
        service_formset = ProviderServiceFormSet(
            request.POST,
            instance=profile
        )

        if form.is_valid() and service_formset.is_valid():
            with transaction.atomic():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()

                user_profile.dni = form.cleaned_data["dni"]
                user_profile.save()

                service_formset.instance = profile
                service_formset.save()

            return redirect("my_provider_services")
    else:
        form = ProviderProfileForm()
        service_formset = ProviderServiceFormSet(
            instance=profile
        )

    return render(
        request,
        "complete-provider-profile.html",
        {
            "form": form,
            "service_formset": service_formset,
        }
    )

@login_required
def add_provider_service(request):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == "POST":
        form = ProviderServiceForm(request.POST)

        if form.is_valid():
            service = form.save(commit=False)
            service.provider = profile
            service.save()

            messages.success(
                request,
                "¡Servicio publicado con éxito!"
            )

            return redirect("my_provider_services")
    else:
        form = ProviderServiceForm()

    return render(
        request,
        "add-provider-service.html",
        {"form": form}
    )
@login_required
def my_provider_services(request):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )
    print("HİZMETLERİ GÖREN:", request.user.username)
    services = ProviderService.objects.filter(
        provider=profile
    )

    return render(
        request,
        "my-provider-services.html",
        {"services": services}
    )
@login_required
def edit_provider_service(request, service_id):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    service = get_object_or_404(
        ProviderService,
        id=service_id,
        provider=profile
    )

    if request.method == "POST":
        form = ProviderServiceForm(request.POST, instance=service)

        if form.is_valid():
            form.save()
            return redirect("my_provider_services")
    else:
        form = ProviderServiceForm(instance=service)

    return render(
        request,
        "edit-provider-service.html",
        {"form": form}
    )
@login_required
def delete_provider_service(request, service_id):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    service = get_object_or_404(
        ProviderService,
        id=service_id,
        provider=profile
    )

    if request.method == "POST":
        service.delete()

    return redirect("my_provider_services")
@login_required
def my_provider_profile(request):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    return render(
        request,
        "my-provider-profile.html",
        {"profile": profile}
    )
@login_required
def edit_provider_profile(request):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    if request.method == "POST":
        form = ProviderProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile_updated")
    else:
        form = ProviderProfileForm(instance=profile)

    return render(
        request,
        "edit-provider-profile.html",
        {"form": form}
    )
@login_required
def profile_updated(request):
    profile = get_object_or_404(
        ProviderProfile,
        user=request.user
    )

    return render(
        request,
        "profile-updated.html",
        {"profile": profile}
    )
@login_required
def edit_phone_number(request):
    user_profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect("phone_updated")
    else:
        form = UserProfileForm(instance=user_profile)

    return render(
        request,
        "edit-phone-number.html",
        {"form": form}
    )
@login_required
def phone_updated(request):
    user_profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    return render(
        request,
        "phone-updated.html",
        {"user_profile": user_profile}
    )