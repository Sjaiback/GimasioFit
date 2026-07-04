from django.http import JsonResponse


def health(request):
    return JsonResponse({"status": "ok", "service": "control-fit-backend"})

# Create your views here.
