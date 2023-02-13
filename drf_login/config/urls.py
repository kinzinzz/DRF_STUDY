from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Apps
    path('admin/', admin.site.urls),
    path('checks/', include('checks.urls')),
    
     # rest-auth
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/signup/', include('rest_auth.registration.urls')),
]
