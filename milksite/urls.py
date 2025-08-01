#milksite/urls.py
from django.contrib import admin
from django.urls import path
from core.views import landing
from django.conf import settings
from django.conf.urls.static import static  
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing'),
    path('milksite/', include('core.urls'))
]
