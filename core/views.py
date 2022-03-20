from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from core.models import Account, PrivateChatRoom
from core.forms import AccountForm, AccountImageUpdateForm
from django.views.generic import View, CreateView
from friends.models import FriendList, FriendRequest
from django.contrib import messages

User = get_user_model()

@receiver(user_signed_up)
def create_account(sender, **kwargs):
    user = kwargs.get('user')
    account = Account.objects.create(user=user)
    account.save()

def delete_account(request):
    user = request.user
    u = User.objects.get(username=user.username)
    u.delete()
    return redirect('/')


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def home(request):
    return render(request, "home.html")

class PanelView(View):

    def get(self, *args, **kwargs):
        context = {}
        account_form = AccountForm()
        account_image_update_form = AccountImageUpdateForm()

        # displaying all avaiable account to give possibility to add friends without knowing username
        people = Account.objects.all()
        context['people'] = people

        # check if user have everything fine with his account and friendlist
        try:
            account = Account.objects.get(user=self.request.user)
            user_friendlist = FriendList.objects.get(user=self.request.user)
        except:
            return HttpResponse("Something wrong.")

        # If everything is fine with account, displaying data to template
        if account:
            context['user_friendlist'] = user_friendlist
            context['id'] = account.id,
            context['username'] = account.user.username,

            # displaying active Friend Requests
            friend_requests = FriendRequest.objects.filter(receiver=self.request.user, is_active=True)
            if friend_requests.exists():
                context['friend_requests'] = friend_requests

            #displaying active chat rooms
            chat_rooms = PrivateChatRoom.objects.filter(user1=self.request.user, is_active=True)
            if chat_rooms.exists():
                context['chat_rooms'] = chat_rooms

            is_self = True
            is_friend = False
            user = self.request.user
            if user.is_authenticated and user != account:
                is_self = False
            elif not user.is_authenticated:
                is_self = False

            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['account'] = account
            context['account_form'] = account_form
            context['account_image_update_form'] = account_image_update_form

        return render(self.request, "empty_panel.html", context)

    def post(self,  *args, **kwargs):
        if self.request.POST:
            account = Account.objects.get(user=self.request.user)
            user = self.request.user

            # add or update account profile infos
            if 'account_update' in self.request.POST:
                account_form = AccountForm(self.request.POST)
                if account_form.is_valid():
                    nationality = account_form.cleaned_data.get('nationality')
                    first_name = account_form.cleaned_data.get('first_name')
                    last_name = account_form.cleaned_data.get('last_name')
                    email = account_form.cleaned_data.get('email')

                    if is_valid_form([nationality, first_name, last_name, email]):
                        account.nationality = nationality
                        account.first_name = first_name
                        account.last_name = last_name
                        user.email = email
                        user.save()
                        account.save()

            # add or update account image
            elif 'image_update' in self.request.POST:
                image_update_form = AccountImageUpdateForm(self.request.POST or None, self.request.FILES or None)
                if image_update_form.is_valid():
                    uploaded_image = image_update_form.cleaned_data.get('account_image')
                    account.account_image = uploaded_image
                    account.save()

            # chat room creating, with default chatroom name
            elif 'create_chat_room' in self.request.POST:
                friend_id = self.request.POST.get('friend_id')
                if friend_id:
                    friend = User.objects.get(id=friend_id)
                    chat_room_qs = PrivateChatRoom.objects.filter(user1=user, user2=friend)
                    if chat_room_qs.exists():
                        messages.info(self.request, "You are chating with this friend already..")
                        return redirect('/panel/')
                    else:
                        chat_room = PrivateChatRoom.objects.create(
                            user1=user,
                            user2=friend,
                            is_active=True,
                        )
                        chat_room.save()
                        return redirect('/panel/')

        return redirect('/')
