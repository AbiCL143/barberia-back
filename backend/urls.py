from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("accounts/", include("allauth.urls")),    
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('emails/', include('emails.urls')),
    # ...
]
