from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect('dashboard')

import accounts.views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', accounts_views.dashboard_view, name='dashboard'),
    path('overlevering/', accounts_views.overlevering_view, name='overlevering'),
    path('cleaning/', accounts_views.cleaning_view, name='cleaning'),
    # Expose Swagger UI at top-level /swagger
    path('swagger/', accounts_views.swagger_ui, name='swagger_ui_root'),
    path('swagger/openapi.yaml', accounts_views.swagger_spec, name='swagger_spec_root'),
    # PT Leads page
    path('pt-leads/', accounts_views.pt_leads_view, name='pt_leads'),
]
