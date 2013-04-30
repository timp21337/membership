from django.contrib import admin
from members.models import Member

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (MemberInline, )


admin.site.register(Member)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)