from django.core.management.base import BaseCommand
from members.models import Member


class Command(BaseCommand):
    args = '<selection selection>'
    help = 'Create text report'

    def handle(self, *args, **options): 
      Member.conditions_m(args[0], args[1:])
