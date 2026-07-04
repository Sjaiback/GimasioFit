from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import StaffProfile


ADMIN = StaffProfile.Role.ADMIN
MANAGER = StaffProfile.Role.MANAGER
RECEPTION = StaffProfile.Role.RECEPTION


def user_role(user):
    if not user.is_authenticated:
        return None
    if user.is_superuser:
        return ADMIN
    profile = getattr(user, "staff_profile", None)
    if not profile or not profile.is_active:
        return None
    return profile.role


def has_role(user, allowed_roles):
    role = user_role(user)
    return bool(role and role in allowed_roles)


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if has_role(request.user, roles):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator
