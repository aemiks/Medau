from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from .models import PrivateChatRoom, PrivateChatRoomMessage, Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_joined',]
    search_fields = ['id', 'user', 'date_joined',]
    readonly_fields = ['date_joined', 'last_login']

admin.site.register(Account, AccountAdmin)

class PrivateChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['id', 'title']

    class Meta:
        model = PrivateChatRoom

admin.site.register(PrivateChatRoom, PrivateChatRoomAdmin)

# Resource: http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class PrivateChatRoomMessageAdmin(admin.ModelAdmin):
    list_filter = ['room', 'user', 'text_date']
    list_display = ['room', 'user', 'text_date', 'text']
    search_fields = ['room__title', 'user__username', 'text']
    readonly_fields = ['id', 'user', 'room', 'text_date']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = PrivateChatRoomMessage

admin.site.register(PrivateChatRoomMessage, PrivateChatRoomMessageAdmin)