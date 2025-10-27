from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default role groups: Receptionist, Manager, Owner, Admin'

    def handle(self, *args, **options):
        roles = ['Receptionist', 'Manager', 'Owner', 'Admin']
        created = []
        for r in roles:
            group, was_created = Group.objects.get_or_create(name=r)
            if was_created:
                created.append(r)

        if created:
            self.stdout.write(self.style.SUCCESS('Created groups: %s' % ', '.join(created)))
        else:
            self.stdout.write('All groups already exist.')
