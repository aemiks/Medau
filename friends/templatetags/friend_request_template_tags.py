from django import template
from friends.models import FriendRequest

register = template.Library()

@register.filter
def friend_request_count(user):
    if user.is_authenticated:
        qs = FriendRequest.objects.filter(receiver=user, is_active=True)
        if qs.exists():
            return qs.count()
    return 0