from django.core.management.base import BaseCommand
from members.models import Member
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--title',
            type="string",
            dest='title',
            default='Iffley Fields Woodcraft Elfins Member',
            help='Title for each page'),
        )
    args = '<selectionType> <selectionName>'
    help = 'Create pdf reports'

    def handle(self, *args, **options):
        Member.output(args[0], args[1:], **options)
