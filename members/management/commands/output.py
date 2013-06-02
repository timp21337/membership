from django.core.management.base import BaseCommand
from members.models import Member


class Command(BaseCommand):
    args = '<selection selection>'
    help = 'Create pdf reports'

    def handle(self, *args, **options):
        Member.output(args[0], args[1:])
