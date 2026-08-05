import json
from json import JSONDecodeError
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from properties.models import (
    Amenity,
    AmenityCategory,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertyType,
)


# =====================================================
# SEED PROPERTY LOOKUPS COMMAND
# =====================================================
class Command(BaseCommand):
    """
    Seeds configurable property lookup records from JSON files.

    The command is idempotent because it uses update_or_create().
    Existing records are updated, while missing records are created.
    """

    help = "Seed Rentora property lookup data."

    # =================================================
    # LOAD JSON FILE
    # =================================================
    def load_json(self, filename):
        """
        Reads and validates a JSON file from properties/data/.

        Returns:
            list: The collection of lookup records contained in the file.

        Raises:
            CommandError: If the file is missing, invalid, or does not
            contain a JSON list.
        """

        file_path = Path(settings.BASE_DIR) / "properties" / "data" / filename

        if not file_path.exists():
            raise CommandError(f"Seed file not found: {file_path}")

        try:
            with file_path.open(
                mode="r",
                encoding="utf-8",
            ) as file:
                records = json.load(file)

        except JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON in {filename}: {exc}") from exc

        except OSError as exc:
            raise CommandError(f"Unable to read {filename}: {exc}") from exc

        if not isinstance(records, list):
            raise CommandError(f"{filename} must contain a JSON list.")

        return records

    # =================================================
    # COMMAND ENTRY POINT
    # =================================================
    @transaction.atomic
    def handle(self, *args, **options):
        """
        Runs all lookup-seeding operations inside one database transaction.

        If any seeding operation fails, all changes made during the command
        are rolled back.
        """

        self.stdout.write("Seeding property lookup data...")

        self.seed_property_types()
        self.seed_property_purposes()
        self.seed_property_conditions()
        self.seed_furnishing_statuses()
        self.seed_amenity_categories()
        self.seed_amenities()

        self.stdout.write(
            self.style.SUCCESS("Property lookup data seeded successfully.")
        )

    # =================================================
    # RECORD RESULT
    # =================================================
    def display_seed_result(
        self,
        *,
        lookup_name,
        created_count,
        updated_count,
    ):
        """
        Displays the number of records created and updated for a lookup.
        """

        self.stdout.write(
            self.style.SUCCESS(
                f"{lookup_name}: "
                f"{created_count} created, "
                f"{updated_count} updated."
            )
        )

    # =================================================
    # SEED PROPERTY TYPES
    # =================================================
    def seed_property_types(self):
        """
        Creates or updates property types.

        Examples:
        - Apartment
        - Duplex
        - Bungalow
        - Land
        """

        records = self.load_json("property_types.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["code", "name"],
                filename="property_types.json",
            )

            _, created = PropertyType.objects.update_or_create(
                code=record["code"],
                defaults={
                    "name": record["name"],
                    "description": record.get("description", ""),
                    "icon": record.get("icon"),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Property types",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # SEED PROPERTY PURPOSES
    # =================================================
    def seed_property_purposes(self):
        """
        Creates or updates property purposes.

        Examples:
        - Rent
        - Sale
        - Short Let
        """

        records = self.load_json("property_purposes.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["code", "name"],
                filename="property_purposes.json",
            )

            _, created = PropertyPurpose.objects.update_or_create(
                code=record["code"],
                defaults={
                    "name": record["name"],
                    "description": record.get("description", ""),
                    "allow_viewing_booking": record.get(
                        "allow_viewing_booking",
                        True,
                    ),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Property purposes",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # SEED PROPERTY CONDITIONS
    # =================================================
    def seed_property_conditions(self):
        """
        Creates or updates property-condition records.

        Examples:
        - Newly Built
        - Newly Renovated
        - Fairly Used
        - Needs Renovation
        """

        records = self.load_json("property_conditions.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["code", "name"],
                filename="property_conditions.json",
            )

            _, created = PropertyCondition.objects.update_or_create(
                code=record["code"],
                defaults={
                    "name": record["name"],
                    "description": record.get("description", ""),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Property conditions",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # SEED FURNISHING STATUSES
    # =================================================
    def seed_furnishing_statuses(self):
        """
        Creates or updates furnishing-status records.

        Examples:
        - Unfurnished
        - Semi Furnished
        - Fully Furnished
        - Serviced
        """

        records = self.load_json("furnishing_statuses.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["code", "name"],
                filename="furnishing_statuses.json",
            )

            _, created = FurnishingStatus.objects.update_or_create(
                code=record["code"],
                defaults={
                    "name": record["name"],
                    "description": record.get("description", ""),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Furnishing statuses",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # SEED AMENITY CATEGORIES
    # =================================================
    def seed_amenity_categories(self):
        """
        Creates or updates categories used to group amenities.

        Examples:
        - Security
        - Utilities
        - Recreation
        - Interior
        """

        records = self.load_json("amenity_categories.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["code", "name"],
                filename="amenity_categories.json",
            )

            _, created = AmenityCategory.objects.update_or_create(
                code=record["code"],
                defaults={
                    "name": record["name"],
                    "description": record.get("description", ""),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Amenity categories",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # SEED AMENITIES
    # =================================================
    def seed_amenities(self):
        """
        Creates or updates amenities and connects each amenity to its
        configured category.

        Examples:
        - Swimming Pool
        - CCTV
        - Elevator
        - Generator
        """

        records = self.load_json("amenities.json")

        created_count = 0
        updated_count = 0

        for index, record in enumerate(records, start=1):
            self.validate_required_fields(
                record=record,
                required_fields=["name", "category"],
                filename="amenities.json",
            )

            category_code = record["category"]

            try:
                category = AmenityCategory.objects.get(
                    code=category_code,
                )
            except AmenityCategory.DoesNotExist as exc:
                raise CommandError(
                    f"Amenity '{record['name']}' references unknown "
                    f"category code '{category_code}'."
                ) from exc

            # Amenity names are globally unique because LookupBaseModel
            # defines name with unique=True.
            _, created = Amenity.objects.update_or_create(
                name=record["name"],
                defaults={
                    "category": category,
                    "description": record.get("description", ""),
                    "icon": record.get("icon"),
                    "display_order": record.get(
                        "display_order",
                        index,
                    ),
                    "is_active": record.get("is_active", True),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.display_seed_result(
            lookup_name="Amenities",
            created_count=created_count,
            updated_count=updated_count,
        )

    # =================================================
    # VALIDATE REQUIRED JSON FIELDS
    # =================================================
    def validate_required_fields(
        self,
        *,
        record,
        required_fields,
        filename,
    ):
        """
        Ensures that each JSON record contains the fields required by
        its corresponding model.
        """

        if not isinstance(record, dict):
            raise CommandError(f"Every record in {filename} must be a JSON object.")

        missing_fields = [
            field
            for field in required_fields
            if field not in record or record[field] in (None, "")
        ]

        if missing_fields:
            missing = ", ".join(missing_fields)

            raise CommandError(
                f"Record in {filename} is missing required "
                f"field(s): {missing}. Record: {record}"
            )
