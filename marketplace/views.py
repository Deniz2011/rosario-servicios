from django.shortcuts import render

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
    return render(request, 'solicitudes.html')
    
def proposal(request):
    return render(request, 'propuesta.html')    

def proposal_sent(request):
    return render(request, 'propuesta-enviada.html')