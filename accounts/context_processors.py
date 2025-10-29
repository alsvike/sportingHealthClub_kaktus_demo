from typing import Dict


def role_flags(request) -> Dict[str, bool]:
    """Expose simple role flags to templates so the sidebar can hide/show links.

    Returns booleans for common groups: Manager, Receptionist, Owner, Admin.
    Superusers are treated as admin.
    """
    user = getattr(request, "user", None)
    flags = {
        "is_manager": False,
        "is_receptionist": False,
        "is_owner": False,
        "is_admin": False,
        "can_view_dashboard": False,
    }

    if not user or not user.is_authenticated:
        return flags

    # superusers get admin privileges and dashboard access
    if getattr(user, "is_superuser", False):
        flags["is_admin"] = True
        flags["can_view_dashboard"] = True
        return flags

    groups = {g.name for g in user.groups.all()}
    flags["is_manager"] = "Manager" in groups
    flags["is_receptionist"] = "Receptionist" in groups
    flags["is_owner"] = "Owner" in groups
    flags["is_admin"] = "Admin" in groups

    # determine dashboard access (managers/owners/admins)
    dashboard_allowed = any(n in groups for n in ["Admin", "Administrator", "Owner", "Manager"])
    flags["can_view_dashboard"] = dashboard_allowed

    return flags
