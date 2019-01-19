from django.core.management import BaseCommand, call_command

from users.models import CustomUser

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata', 'users')
        # Fix the passwords of fixtures
        for user in CustomUser.objects.all():
            user.set_password(user.password)
            user.save()
