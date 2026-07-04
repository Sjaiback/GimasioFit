from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/members/", include("members.urls")),
    path("api/memberships/", include("memberships.urls")),
    path("api/billing/", include("billing.urls")),
    path("api/attendance/", include("attendance.urls")),
    path("api/reports/", include("reports.urls")),
    path("api/notifications/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
