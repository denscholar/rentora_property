from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from locations.models import Area

from properties.models import (
    Amenity,
    FurnishingStatus,
    PropertyCondition,
    PropertyPurpose,
    PropertyType,
)


@dataclass(slots=True)
class SubmissionDraftDTO:
    """
    Represents validated submission data passed from serializers
    into the service layer.

    Every field is optional because drafts may be incomplete.
    """

    property_type: PropertyType | None = None
    purpose: PropertyPurpose | None = None
    property_condition: PropertyCondition | None = None
    furnishing_status: FurnishingStatus | None = None

    area: Area | None = None

    payment_frequency: str | None = None

    title: str = ""

    description: str = ""

    landmark: str = ""

    street_address: str = ""

    bedrooms: int = 0
    bathrooms: int = 0
    toilets: int = 0
    parking_spaces: int = 0

    floors: int = 0

    units_available: int = 1

    year_built: int | None = None

    is_new_build: bool = False

    is_serviced: bool = False

    is_negotiable: bool = False

    land_size: Decimal | None = None

    building_size: Decimal | None = None

    size_unit: str | None = None

    available_from: date | None = None

    minimum_stay: int | None = None

    proposed_price: Decimal | None = None

    service_charge: Decimal = Decimal("0")

    caution_fee: Decimal = Decimal("0")

    legal_fee: Decimal = Decimal("0")

    agency_fee: Decimal = Decimal("0")

    latitude: float | None = None

    longitude: float | None = None

    amenities: list[Amenity] | None = None