from django.shortcuts import render, HttpResponse, redirect
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from friends.models import FriendList, FriendRequest
from core.models import Account
from django.contrib import messages


@receiver(user_signed_up)
def create_friendlist(sender, **kwargs):
    user = kwargs.get('user')
    friendlist = FriendList.objects.create(user=user)
    friendlist.save()


def send_friend_request(request, *args, **kwargs):
    user = request.user
    if request.method == "POST":
        user_id = request.POST.get('receiver_user_id')
        if user_id:
            receiver = Account.objects.get(id=user_id)
            friend_request = FriendRequest.objects.filter(sender=user, receiver=receiver.user)
            if friend_request:
                #check if there is already a friend request to this user
                for f_request in friend_request:
                    if f_request.is_active:
                        #check is it active friend request.
                        messages.warning(request, "You already send a friend request to this user.")
                        return redirect('/panel/')
                    else:
                        #if there is no active friend request - create a new one
                        friend_request = FriendRequest.objects.create(sender=user, receiver=receiver.user,
                                                                      is_active=True)
                        friend_request.save()
                        messages.success(request, "Friend request sent.")
                        return redirect('/panel/')
            else:
                # There are no friend request so create new one.
                friend_request = FriendRequest.objects.create(sender=user, receiver=receiver.user, is_active=True)
                friend_request.save()
                messages.success(request, "Friend request sent.")
                return redirect("/panel/")
        else:
            messages.error(request, "Unable to send a friend request.")
            return redirect("/panel/")
    else:
        messages.error(request,"You must be authenticated")
    return redirect("/panel/")

def accept_friend_request(request, id):
    friend_request_id = id
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.accept()
    return redirect("/panel/")

def decline_friend_request(request, id):
    friend_request_id = id
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.decline()
    return redirect("/panel/")