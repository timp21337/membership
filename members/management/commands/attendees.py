from django.core.management.base import BaseCommand
from members.models import Member


class Command(BaseCommand):
    args = '<session_name session_name_id>'
    help = 'Create pdf reports for attendees'

    def handle(self, *args, **options):
        Member.output('attendees', args[0])
