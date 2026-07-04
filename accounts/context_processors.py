from .security import ADMIN, MANAGER, RECEPTION, user_role


def staff_role(request):
    role = user_role(request.user)
    return {
        "current_role": role,
        "role_admin": ADMIN,
        "role_manager": MANAGER,
        "role_reception": RECEPTION,
        "can_manage": role in {ADMIN, MANAGER},
    }
