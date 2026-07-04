from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .services import administrative_metrics, dashboard_metrics


@require_http_methods(["GET"])
def administrative_report(request):
    return JsonResponse(administrative_metrics())


@require_http_methods(["GET"])
def dashboard(request):
    return JsonResponse(dashboard_metrics())

# Create your views here.
