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
        "is_administrator": False,
        "can_view_dashboard": False,
        "can_view_pt_leads": False,
    }

    if not user or not user.is_authenticated:
        return flags

    # superusers get admin privileges and dashboard access
    if getattr(user, "is_superuser", False):
        flags["is_admin"] = True
        flags["can_view_dashboard"] = True
        # superusers also can view PT Leads
        flags["can_view_pt_leads"] = True
        return flags

    groups = {g.name for g in user.groups.all()}
    flags["is_manager"] = "Manager" in groups
    flags["is_receptionist"] = "Receptionist" in groups
    flags["is_owner"] = "Owner" in groups
    flags["is_admin"] = "Admin" in groups
    flags["is_administrator"] = "Administrator" in groups

    # determine dashboard access (managers/owners/admins)
    dashboard_allowed = any(n in groups for n in ["Admin", "Administrator", "Owner", "Manager"])
    flags["can_view_dashboard"] = dashboard_allowed

    # PT Leads allowed for Owner, Manager, Receptionist, Admin, Administrator
    flags["can_view_pt_leads"] = any(n in groups for n in ["Owner", "Manager", "Receptionist", "Admin", "Administrator"]) 

    return flags
