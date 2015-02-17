from django.core.management.base import BaseCommand
from members.models import Member


class Command(BaseCommand):
    args = '<selection>'
    help = 'Print CSV for selection'

    def handle(self, *args, **options):
        Member.csv(args[0])
