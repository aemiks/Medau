from django.urls import path
from .views import PanelView, delete_account, home
from django.conf.urls.static import static
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', home, name="home"),
    path('panel/', PanelView.as_view(), name="panel"),
    path('delete/', delete_account, name="delete_account" )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)