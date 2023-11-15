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

from django.conf.urls.static import static
from esoft import settings
from django.contrib import admin
from django.urls import path, include
from mainapp.views import registration, client_registration, realtor_registration, home, profile, real_estate, create_an_apartment, create_a_house, create_land, logout_user, search_offers_demands, create_offer, create_demand, deals, manage_clients

urlpatterns = [
    path("admin/", admin.site.urls),

    path('registration/', registration, name='registration'),

    path('logout/', logout_user, name='logout'),

    path('client_registration/', client_registration, name='client_registration'),

    path('realtor_registration/', realtor_registration, name='realtor_registration'),
    
    path('', include('django.contrib.auth.urls')),

    path('profile/', profile, name='profile'),

    path('', home, name='home'),
    
    path('real_estate/', real_estate, name='real_estate'),

    path('create_an_apartment/', create_an_apartment, name='create_an_apartment'),
    
    path('create_a_house/', create_a_house, name='create_a_house'),

    path('create_land/', create_land, name='create_land'),

    path('search_offers_demands/', search_offers_demands, name='search_offers_demands'),

    path('create_offer/', create_offer, name='create_offer'),

    path('create_demand/', create_demand, name='create_demand'),

    path('deals/', deals, name='deals'),

    path('api-auth/', include('rest_framework.urls')),

    path('manage_clients/', manage_clients, name='manage_clients'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)