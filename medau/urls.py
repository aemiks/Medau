
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('', include('agora.urls', namespace='agora')),
    path('', include('friends.urls', namespace='friends')),
]
