from django.contrib import admin
from members.models import Member, Attendance, Session

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False


class AttendanceTabularInline(admin.TabularInline):
    model = Attendance
    fk_name = 'session'

class UserAdmin(UserAdmin):
    inlines = [MemberInline]


class SessionAdmin(admin.ModelAdmin):
    inlines = [AttendanceTabularInline]

admin.site.register(Member)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)