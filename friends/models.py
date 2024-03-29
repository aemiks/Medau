from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect


class FriendList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="user_friendlist")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True,
                                     null=True,
                                     related_name="friends")

    def __str__(self):
        return self.user.username

    def count_friends(self):
        """
        Return number of friends
        """
        return self.friends.all().count()

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initate the action of unfriend someone
        """
        remover_friends_list = self # person terminating the friendship

        #remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # remove friend from removee friend list
        friend_list = FriendList.objects.get(user=removee)
        friend_list.remove_friend(remover_friends_list.user)

    def is_mutual_friend(self, friend):
        """
        Is this friend?
        """
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    A friend request cons of 2 main parts:
        1. sender:
            - person who sending the friend request
        2. receiver:
            - person receiving the friend request
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="receiver")
    is_active = models.BooleanField(blank=False, null= False, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Acccept friend request
        Update Sander and Reciver friend_list
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        It is decline by setting is_active field to False
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel friend request
        It is cancelled by setting is_active field to False.
        Its only different with respect to declaning through the notification that is generated.
        """
        self.is_active = False
        self.save()
