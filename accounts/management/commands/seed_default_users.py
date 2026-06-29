# accounts/management/commands/seed_default_users.py

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser


# ==========================================
# SEED DEFAULT USERS COMMAND
# ==========================================
class Command(BaseCommand):
    help = "Create default Rentora demo users."

    def handle(self, *args, **options):
        default_password = "Password@123"

        users = [
            {
                "email": "admin@rentora.com",
                "phone_number": "2348000000001",
                "first_name": "Rentora",
                "last_name": "Admin",
                "role": CustomUser.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "is_verified": True,
            },
            {
                "email": "tenant@rentora.com",
                "phone_number": "2348000000002",
                "first_name": "Demo",
                "last_name": "Tenant",
                "role": CustomUser.Role.TENANT,
                "is_verified": True,
            },
            {
                "email": "agent@rentora.com",
                "phone_number": "2348000000003",
                "first_name": "Demo",
                "last_name": "Agent",
                "role": CustomUser.Role.AGENT,
                "is_verified": True,
            },
            {
                "email": "landlord@rentora.com",
                "phone_number": "2348000000004",
                "first_name": "Demo",
                "last_name": "Landlord",
                "role": CustomUser.Role.LANDLORD,
                "is_verified": True,
            },
        ]

        with transaction.atomic():
            for data in users:
                email = data["email"]

                user, created = CustomUser.objects.get_or_create(
                    email=email,
                    defaults={
                        **data,
                    },
                )

                if created:
                    user.set_password(default_password)
                    user.save(update_fields=["password"])

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created user: {email}"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"User already exists: {email}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Default Rentora users seeding completed."
            )
        )

# python manage.py seed_default_users