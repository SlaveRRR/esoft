"""esoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from mainapp.views import client_registration, realtor_registration, home, profile, real_estate, create_an_apartment, create_a_house, create_land

urlpatterns = [
    path("admin/", admin.site.urls),

    path('client_registration/', client_registration, name='client_registration'),

    path('realtor_registration/', realtor_registration, name='realtor_registration'),
    
    path('', include('django.contrib.auth.urls')),

    path('profile/', profile, name='profile'),

    path('home/', home, name='home'),
    
    path('real_estate/', real_estate, name='real_estate'),

    path('create_an_apartment/', create_an_apartment, name='create_an_apartment'),
    
    path('create_a_house/', create_a_house, name='create_a_house'),

    path('create_land/', create_land, name='create_land'),

]
