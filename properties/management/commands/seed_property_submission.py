from decimal import Decimal
from datetime import date, timedelta
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from properties.models import PropertySubmission
from properties.models.lookups import PropertyPurpose, PropertyType
from properties.models.lookups.amenity import Amenity
from properties.models.lookups.furnishing_status import FurnishingStatus
from properties.models.lookups.property_condition import PropertyCondition
from locations.models import Area
from properties.models.property.submission import PaymentFrequency, SizeUnit


class Command(BaseCommand):
    help = "Seed 30 property submission records for testing."

    PROPERTY_DATA = [
        {
            "title": "2 Bedroom Apartment",
            "area": "Guzape",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "2000000.00",
        },
        {
            "title": "4 Bedroom Duplex in Life Camp",
            "area": "Life Camp",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 4,
            "toilets": 5,
            "parking_spaces": 4,
            "price": "9000000.00",
        },
        {
            "title": "3 Bedroom Apartment",
            "area": "Wuse 2",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "4500000.00",
        },
        {
            "title": "5 Bedroom Detached Duplex",
            "area": "Maitama",
            "property_type": "Detached Duplex",
            "purpose": "Rent",
            "bedrooms": 5,
            "bathrooms": 5,
            "toilets": 6,
            "parking_spaces": 5,
            "price": "18000000.00",
        },
        {
            "title": "3 Bedroom Terrace Duplex",
            "area": "Jabi",
            "property_type": "Terrace",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 3,
            "price": "7000000.00",
        },
        {
            "title": "2 Bedroom Apartment",
            "area": "Gwarinpa",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "1800000.00",
        },
        {
            "title": "4 Bedroom Duplex",
            "area": "Katampe",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 4,
            "toilets": 5,
            "parking_spaces": 4,
            "price": "12000000.00",
        },
        {
            "title": "3 Bedroom Apartment",
            "area": "Lokogoma",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "3200000.00",
        },
        {
            "title": "Mini Flat",
            "area": "Garki",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 1,
            "bathrooms": 1,
            "toilets": 1,
            "parking_spaces": 1,
            "price": "1500000.00",
        },
        {
            "title": "Luxury 4 Bedroom Duplex",
            "area": "Asokoro",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 5,
            "toilets": 6,
            "parking_spaces": 4,
            "price": "20000000.00",
        },
        {
            "title": "2 Bedroom Serviced Apartment",
            "area": "Maitama",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "6500000.00",
        },
        {
            "title": "3 Bedroom Terrace Duplex",
            "area": "Wuye",
            "property_type": "Terrace",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 3,
            "price": "5500000.00",
        },
        {
            "title": "4 Bedroom Detached Duplex",
            "area": "Karsana",
            "property_type": "Detached Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 4,
            "toilets": 5,
            "parking_spaces": 4,
            "price": "8500000.00",
        },
        {
            "title": "3 Bedroom Apartment",
            "area": "Utako",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "4000000.00",
        },
        {
            "title": "5 Bedroom Luxury Duplex",
            "area": "Katampe Extension",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 5,
            "bathrooms": 5,
            "toilets": 6,
            "parking_spaces": 6,
            "price": "22000000.00",
        },
        {
            "title": "2 Bedroom Flat",
            "area": "Kubwa",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "1400000.00",
        },
        {
            "title": "3 Bedroom Apartment",
            "area": "Apo",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "2800000.00",
        },
        {
            "title": "4 Bedroom Terrace Duplex",
            "area": "Galadimawa",
            "property_type": "Terrace",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 4,
            "toilets": 5,
            "parking_spaces": 3,
            "price": "6000000.00",
        },
        {
            "title": "2 Bedroom Apartment",
            "area": "Mabushi",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "3000000.00",
        },
        {
            "title": "6 Bedroom Detached Duplex",
            "area": "Asokoro",
            "property_type": "Detached Duplex",
            "purpose": "Rent",
            "bedrooms": 6,
            "bathrooms": 6,
            "toilets": 7,
            "parking_spaces": 7,
            "price": "30000000.00",
        },
        {
            "title": "3 Bedroom Flat",
            "area": "Apo Resettlement",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "2500000.00",
        },
        {
            "title": "4 Bedroom Duplex",
            "area": "Dawaki",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 4,
            "toilets": 5,
            "parking_spaces": 4,
            "price": "7000000.00",
        },
        {
            "title": "2 Bedroom Apartment",
            "area": "Jahi",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "2800000.00",
        },
        {
            "title": "3 Bedroom Luxury Apartment",
            "area": "Wuse 2",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 3,
            "price": "6000000.00",
        },
        {
            "title": "4 Bedroom Detached House",
            "area": "Guzape",
            "property_type": "Detached Duplex",
            "purpose": "Rent",
            "bedrooms": 4,
            "bathrooms": 5,
            "toilets": 6,
            "parking_spaces": 4,
            "price": "15000000.00",
        },
        {
            "title": "Mini Flat",
            "area": "Garki",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 1,
            "bathrooms": 1,
            "toilets": 1,
            "parking_spaces": 1,
            "price": "1200000.00",
        },
        {
            "title": "3 Bedroom Terrace Duplex",
            "area": "Karsana",
            "property_type": "Terrace",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 3,
            "price": "5000000.00",
        },
        {
            "title": "2 Bedroom Serviced Flat",
            "area": "Jabi",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 2,
            "bathrooms": 2,
            "toilets": 2,
            "parking_spaces": 2,
            "price": "5000000.00",
        },
        {
            "title": "5 Bedroom Duplex",
            "area": "Life Camp",
            "property_type": "Duplex",
            "purpose": "Rent",
            "bedrooms": 5,
            "bathrooms": 5,
            "toilets": 6,
            "parking_spaces": 5,
            "price": "14000000.00",
        },
        {
            "title": "3 Bedroom Apartment",
            "area": "Gwarinpa",
            "property_type": "Apartment",
            "purpose": "Rent",
            "bedrooms": 3,
            "bathrooms": 3,
            "toilets": 4,
            "parking_spaces": 2,
            "price": "2500000.00",
        },
    ]

    STATUS_DISTRIBUTION = [
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.DRAFT,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.UNDER_REVIEW,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.APPROVED,
        PropertySubmission.Status.REJECTED,
        PropertySubmission.Status.REJECTED,
        PropertySubmission.Status.REJECTED,
        PropertySubmission.Status.REJECTED,
        PropertySubmission.Status.REJECTED,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
        PropertySubmission.Status.MORE_INFORMATION_REQUIRED,
        PropertySubmission.Status.DUPLICATE_FOUND,
        PropertySubmission.Status.DUPLICATE_FOUND,
    ]

    def handle(self, *args, **options):
        User = get_user_model()

        user = User.objects.filter(is_active=True).first()

        if not user:
            self.stdout.write(
                self.style.ERROR("No active user found. Create a user first.")
            )
            return

        self.stdout.write(self.style.WARNING(f"Using user: {user}"))

        property_types = {obj.name.lower(): obj for obj in PropertyType.objects.all()}

        purposes = {obj.name.lower(): obj for obj in PropertyPurpose.objects.all()}

        areas = {obj.name.lower(): obj for obj in Area.objects.all()}

        conditions = list(PropertyCondition.objects.all())
        furnishings = list(FurnishingStatus.objects.all())
        amenities = list(Amenity.objects.all())

        if not property_types:
            self.stdout.write(self.style.ERROR("No PropertyType records found."))
            return

        if not purposes:
            self.stdout.write(self.style.ERROR("No PropertyPurpose records found."))
            return

        if not areas:
            self.stdout.write(self.style.ERROR("No Area records found."))
            return

        created_count = 0

        for index, property_data in enumerate(self.PROPERTY_DATA):
            status = self.STATUS_DISTRIBUTION[index]

            property_type = self.get_lookup(
                property_types,
                property_data["property_type"],
            )

            purpose = self.get_lookup(
                purposes,
                property_data["purpose"],
            )

            area = self.get_lookup(
                areas,
                property_data["area"],
            )

            if not property_type:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping {property_data['title']}: "
                        f"PropertyType '{property_data['property_type']}' "
                        f"not found."
                    )
                )
                continue

            if not purpose:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping {property_data['title']}: "
                        f"PropertyPurpose '{property_data['purpose']}' "
                        f"not found."
                    )
                )
                continue

            if not area:
                self.stdout.write(
                    self.style.WARNING(
                        f"Skipping {property_data['title']}: "
                        f"Area '{property_data['area']}' "
                        f"not found."
                    )
                )
                continue

            condition = random.choice(conditions) if conditions else None

            furnishing = random.choice(furnishings) if furnishings else None

            submission = PropertySubmission.objects.create(
                submitted_by=user,
                source=PropertySubmission.Source.AGENT,
                property_type=property_type,
                purpose=purpose,
                area=area,
                property_condition=condition,
                furnishing_status=furnishing,
                title=property_data["title"],
                description=(
                    f"Well maintained {property_data['bedrooms']} "
                    f"bedroom property located in "
                    f"{property_data['area']}, Abuja. "
                    "Suitable for residential living with good "
                    "access to major roads and nearby amenities."
                ),
                landmark=(f"Close to major facilities in " f"{property_data['area']}"),
                street_address=(
                    f"{random.randint(1, 99)} "
                    f"{random.choice(['Main Street', 'Garden Avenue', 'Close', 'Crescent'])}, "
                    f"{property_data['area']}, Abuja"
                ),
                bedrooms=property_data["bedrooms"],
                bathrooms=property_data["bathrooms"],
                toilets=property_data["toilets"],
                parking_spaces=property_data["parking_spaces"],
                size_unit=SizeUnit.SQUARE_METERS,
                land_size=Decimal(random.randint(180, 850)),
                building_size=Decimal(random.randint(90, 600)),
                payment_frequency=PaymentFrequency.ANNUALLY,
                proposed_price=Decimal(property_data["price"]),
                service_charge=Decimal(
                    random.choice(
                        [
                            "100000",
                            "150000",
                            "200000",
                            "250000",
                            "300000",
                        ]
                    )
                ),
                caution_fee=Decimal(
                    random.choice(
                        [
                            "100000",
                            "150000",
                            "200000",
                        ]
                    )
                ),
                legal_fee=Decimal(
                    random.choice(
                        [
                            "100000",
                            "150000",
                            "200000",
                        ]
                    )
                ),
                agency_fee=Decimal(
                    random.choice(
                        [
                            "200000",
                            "250000",
                            "300000",
                        ]
                    )
                ),
                status=status,
                floors=random.choice(
                    [
                        1,
                        1,
                        2,
                        2,
                        3,
                    ]
                ),
                units_available=random.choice(
                    [
                        1,
                        1,
                        1,
                        2,
                    ]
                ),
                year_built=random.randint(
                    2010,
                    2025,
                ),
                is_new_build=random.choice(
                    [
                        False,
                        False,
                        False,
                        True,
                    ]
                ),
                is_serviced=random.choice(
                    [
                        False,
                        False,
                        True,
                    ]
                ),
                is_negotiable=property_data.get(
                    "is_negotiable",
                    random.choice([True, False]),
                ),
                available_from=(date.today() + timedelta(days=random.randint(0, 60))),
                minimum_stay=(
                    12 if status != PropertySubmission.Status.DRAFT else None
                ),
            )

            if amenities:
                selected_amenities = random.sample(
                    amenities,
                    min(
                        random.randint(2, 5),
                        len(amenities),
                    ),
                )

                submission.amenities.set(selected_amenities)

            if status == PropertySubmission.Status.APPROVED:
                submission.review_note = (
                    "Property verified and approved " "for listing."
                )
                submission.reviewed_by = user
                submission.reviewed_at = submission.updated_at

            elif status == PropertySubmission.Status.REJECTED:
                submission.review_note = random.choice(
                    [
                        "Property information could not be verified.",
                        "Submitted property details require correction.",
                        "Property does not currently meet listing requirements.",
                    ]
                )
                submission.reviewed_by = user
                submission.reviewed_at = submission.updated_at

            elif status == PropertySubmission.Status.MORE_INFORMATION_REQUIRED:
                submission.review_note = random.choice(
                    [
                        "Please provide clearer property documentation.",
                        "Additional property information is required.",
                        "Please provide more details about the property.",
                    ]
                )
                submission.reviewed_by = user
                submission.reviewed_at = submission.updated_at

            elif status == PropertySubmission.Status.DUPLICATE_FOUND:
                submission.duplicate_similarity_score = Decimal(
                    random.choice(
                        [
                            "86.50",
                            "91.20",
                            "94.75",
                            "97.10",
                        ]
                    )
                )

                submission.review_note = (
                    "A potentially duplicate property " "was identified."
                )

                submission.reviewed_by = user
                submission.reviewed_at = submission.updated_at

            submission.save(
                update_fields=[
                    "review_note",
                    "reviewed_by",
                    "reviewed_at",
                    "duplicate_similarity_score",
                ]
            )

            created_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{created_count}/30] "
                    f"{submission.title} "
                    f"({submission.get_status_display()})"
                )
            )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} " "property submissions."
            )
        )

    @staticmethod
    def get_lookup(lookup_dict, value):
        """
        Resolve a lookup by name, case-insensitively.
        """
        return lookup_dict.get(str(value).strip().lower())
