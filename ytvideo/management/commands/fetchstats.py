from django.core.management.base import BaseCommand
from django.conf import settings
import os

import environ
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

class Command(BaseCommand):
    help = "Fetches youtube video stats for chanels defined"

    def handle(self, *args, **options):
        self.stdout.write("Fetching video statsS...")
        self.stdout.write("Channels: %s" % (env("CHANNEL_LIST")))
