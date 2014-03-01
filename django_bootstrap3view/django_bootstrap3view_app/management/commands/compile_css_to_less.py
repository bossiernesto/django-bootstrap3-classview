__author__ = 'ernesto'

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from lib.css_to_less import CSSConverter

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.do_run(*args)

    def do_run(self, *args):
        #TODO: convert css files
        builder = CSSConverter('../../bootstrap')
        builder.build()
