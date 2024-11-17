"""
URL configuration for demo_task project.

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
from api.views import (
    ClientListView,ClientCreateView,ClientDetailView,ClientUpdateView,
    ClientDeleteView,CreateProjectView,UserProjectsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('createclients/', ClientCreateView.as_view(), name='client-create'),
    path('getclients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('updateclients/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('deleteclients/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),
    path('createproject/<int:id>/projects/', CreateProjectView.as_view(), name='create-project'),
    path('projects/', UserProjectsView.as_view(), name='user-projects'),
]
