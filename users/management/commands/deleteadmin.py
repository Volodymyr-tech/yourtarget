from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        try:
            admin_user = User.objects.get(
                username="supermanager"
            )
            admin_user.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user deleted: {admin_user.username}"
                )
            )
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Could not find admin user to delete it"))