from django.urls import path
from .views import send_friend_request, accept_friend_request, decline_friend_request
from django.conf.urls.static import static
from django.conf import settings

app_name = 'friends'

urlpatterns = [
    path('friend_request/', send_friend_request, name="send_friend_request" ),
    path('accept_friend_request/<id>',accept_friend_request, name="accept_friend_request"),
    path('decline_friend_request/<id>',decline_friend_request, name="decline_friend_request"),
]