from django.core.management.base import BaseCommand

import environ
env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    help = "Fetches youtube video stats for chanels defined"

    def handle(self, *args, **options):
        self.stdout.write("Fetching video statsS...")
        self.stdout.write("Channels: %s" % (env("CHANNEL_LIST")))
