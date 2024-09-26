"""
URL configuration for parish_inspection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inspections import views as inspection_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inspection_views.home, name='home'),
    path('register/', inspection_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='inspections/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inspections/logout.html'), name='logout'),
    path('parish/create/', inspection_views.create_parish, name='create_parish'),
    path('parish/<int:parish_id>/', inspection_views.parish_detail, name='parish_detail'),
    path('parish/<int:parish_id>/inspection/create/', inspection_views.create_inspection, name='create_inspection'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/', inspection_views.inspection_detail, name='inspection_detail'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/edit/', inspection_views.edit_inspection, name='edit_inspection'),
    path('parish/<int:parish_id>/inspection/<int:inspection_id>/delete/', inspection_views.delete_inspection, name='delete_inspection'),
]

