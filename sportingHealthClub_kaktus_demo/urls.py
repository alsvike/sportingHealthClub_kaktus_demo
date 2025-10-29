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
]
