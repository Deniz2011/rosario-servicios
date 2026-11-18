from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import ServiceRequest, Proposal

def home(request):
    return render(request, 'index.html')

def need_service(request):
    return render(request, 'hizmet-ariyorum.html')
    
def offer_service(request):
    return render(request, 'hizmet-veriyorum.html')

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
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )