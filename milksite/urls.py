#milksite/urls.py
from django.contrib import admin
from django.urls import path
from core.views import main
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('milksite/', include('core.urls'))
]
