from pathlib import Path
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from locations.models import Country, State, LGA, Area


class Command(BaseCommand):

    help = "Import location dataset."

    @transaction.atomic
    def handle(self, *args, **kwargs):

        dataset = (
            Path(settings.BASE_DIR)
            / "locations"
            / "data"
            / "nigeria.json"
        )

        with open(dataset, encoding="utf-8") as file:
            data = json.load(file)

        country, _ = Country.objects.get_or_create(
            code=data["country"]["code"],
            defaults={
                "name": data["country"]["name"],
            },
        )

        for state_data in data["states"]:

            state, _ = State.objects.get_or_create(
                country=country,
                name=state_data["name"],
            )

            for lga_data in state_data["lgas"]:

                lga, _ = LGA.objects.get_or_create(
                    state=state,
                    name=lga_data["name"],
                )

                for area_data in lga_data["areas"]:

                    Area.objects.get_or_create(
                        lga=lga,
                        name=area_data["name"],
                        defaults={
                            "latitude": area_data.get("latitude"),
                            "longitude": area_data.get("longitude"),
                        },
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Locations imported successfully."
            )
        )