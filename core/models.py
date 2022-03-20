from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

User = get_user_model()

def get_account_image_filepath(self, filename):
	return 'account_images/' + str(self.pk) + '/account_image.png'

def get_default_account_image():
	return "img/user-solid.svg"


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    account_image = models.ImageField(max_length=255,
                                      upload_to=get_account_image_filepath,
                                      null=True,
                                      blank=True,
                                      default=get_default_account_image)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nationality = CountryField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_account_image_filename(self):
        return str(self.account_image)[str(self.account_image).index('account_images/' + str(self.pk) + "/"):]


class PrivateChatRoom(models.Model):
    title = models.CharField(max_length=20, default="Private Chat")
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                              null=True,
                              related_name="user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                              null=True,
                              related_name="user2")
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def connect_user(self, user):
        """
        return True if user is added to chat
        """
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect_user(self, user):
        """
        return True if user is disconnected from the chat
        """
        is_user_removed = False
        if not user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """
        return the channels group name that sockets should subscribe to and get sent
        messages as they are generated.
        """
        return f"PrivateChatRoom-{self.id}"

class PrivateChatRoomMessageManager(models.Manager):
    def by_room(self, room):
        qs = PrivateChatRoomMessage.objects.filter(room=room).order_by("-text_date")
        return qs

class PrivateChatRoomMessage(models.Model):
    """
    Chat message created by a user inside a PrivateChatRoom
    """
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    text = models.TextField(max_length=500, unique=False, blank=False)
    text_date = models.DateTimeField(auto_now_add=True)

    objects = PrivateChatRoomMessageManager()

    def __str__(self):
        return self.text

