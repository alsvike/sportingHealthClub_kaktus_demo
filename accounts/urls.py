from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-login-redirect/', views.post_login_redirect, name='post_login_redirect'),
    path('swagger/', views.swagger_ui, name='swagger_ui'),
    path('swagger/openapi.yaml', views.swagger_spec, name='swagger_spec'),
]

# separate small urlconf for dashboard to keep project urls tidy
urlpatterns_dashboard = [
    path('', views.dashboard_view, name='dashboard'),
]

# API endpoints used by the Overlevering calendar (JSON)
api_urlpatterns = [
    path('api/day/', views.api_day_data, name='api_day_data'),
    path('api/trials/', views.api_create_trial, name='api_create_trial'),
    path('api/trials/<int:pk>/', views.api_modify_trial, name='api_modify_trial'),
    path('api/cleaning/', views.api_cleaning_update, name='api_cleaning_update'),
    path('api/cleaning_tasks/', views.api_cleaning_tasks, name='api_cleaning_tasks'),
    path('api/cleaning_tasks/<int:pk>/', views.api_modify_cleaning_task, name='api_modify_cleaning_task'),
    path('api/shift_message/', views.api_shift_message, name='api_shift_message'),
    path('api/manager_message/', views.api_manager_message, name='api_manager_message'),
]

# expose API endpoints on the same `accounts/` prefix
urlpatterns += api_urlpatterns
