from django.core.management.base import BaseCommand
from django.db import transaction

from locations.models import Country, State, City, Area


# =====================================================
# SEED LOCATIONS COMMAND
# =====================================================
class Command(BaseCommand):
    help = "Seed default Rentora locations."

    def handle(self, *args, **options):
        areas = [
            "Wuse",
            "Wuse 2",
            "Garki",
            "Garki 2",
            "Maitama",
            "Asokoro",
            "Gwarinpa",
            "Jabi",
            "Utako",
            "Kubwa",
            "Lugbe",
            "Lokogoma",
            "Apo",
            "Guzape",
            "Katampe",
            "Kado",
            "Life Camp",
            "Jahi",
            "Durumi",
            "Galadimawa",
            "Gaduwa",
            "Dawaki",
            "Mpape",
            "Karsana",
            "Kuje",
        ]

        with transaction.atomic():
            country, _ = Country.objects.get_or_create(
                name="Nigeria",
                defaults={
                    "code": "NG",
                    "display_order": 1,
                },
            )

            state, _ = State.objects.get_or_create(
                country=country,
                name="Federal Capital Territory",
                defaults={
                    "display_order": 1,
                },
            )

            city, _ = City.objects.get_or_create(
                state=state,
                name="Abuja",
                defaults={
                    "display_order": 1,
                },
            )

            for index, area_name in enumerate(areas, start=1):
                Area.objects.get_or_create(
                    city=city,
                    name=area_name,
                    defaults={
                        "display_order": index,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Default locations seeded successfully."
            )
        )