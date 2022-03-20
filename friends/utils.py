from friends.models import FriendRequest

def get_friend_request_or_false(sender, receiver):
    try:
        return FriendRequest.object.get(sender=sender,
                                        receicer=receiver,
                                        is_active=True)
    except FriendRequest.DoesNotExist:
        return False