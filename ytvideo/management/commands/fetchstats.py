from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Fetches youtube video stats for chanels defined"

    def handle(self, *args, **options):
        self.stdout.write("Fetching video stats...") 
