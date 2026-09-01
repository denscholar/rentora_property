from properties.matching.category import resolve_property_category
from properties.matching.normalization import (
    normalize_address,
    normalize_landmark,
    normalize_text,
    normalize_title,
)


def get_submission_representation(submission):
    """
    Convert a PropertySubmission into a normalized dictionary
    used by the matching engine.
    """

    property_type = submission.property_type
    purpose = submission.purpose
    area = submission.area

    category = resolve_property_category(
        property_type,
    )

    return {
        # ----------------------------------------------------
        # BASIC IDENTITY
        # ----------------------------------------------------
        "uuid": str(submission.uuid),
        "title": normalize_title(
            submission.title,
        ),
        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------
        "category": category,
        # ----------------------------------------------------
        # LOOKUPS
        # ----------------------------------------------------
        "property_type": normalize_text(getattr(property_type, "name", "")),
        "purpose": normalize_text(getattr(purpose, "name", "")),
        "area": normalize_text(getattr(area, "name", "")),
        # ----------------------------------------------------
        # PROPERTY CHARACTERISTICS
        # ----------------------------------------------------
        "bedrooms": submission.bedrooms,
        "bathrooms": submission.bathrooms,
        "toilets": submission.toilets,
        "parking_spaces": submission.parking_spaces,
        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------
        "landmark": normalize_landmark(
            submission.landmark,
        ),
        "street_address": normalize_address(
            submission.street_address,
        ),
        # ----------------------------------------------------
        # PROPERTY SIZE
        # ----------------------------------------------------
        "size_unit": normalize_text(
            submission.size_unit,
        ),
        "land_size": submission.land_size,
        "building_size": submission.building_size,
        # ----------------------------------------------------
        # PRICING
        # ----------------------------------------------------
        "proposed_price": submission.proposed_price,
        "payment_frequency": normalize_text(
            submission.payment_frequency,
        ),
        # ----------------------------------------------------
        # PROPERTY FLAGS
        # ----------------------------------------------------
        "is_new_build": submission.is_new_build,
        "is_serviced": submission.is_serviced,
        "is_negotiable": submission.is_negotiable,
        # ----------------------------------------------------
        # ESTATE / UNIT INFORMATION
        # ----------------------------------------------------
        "floors": submission.floors,
        "units_available": submission.units_available,
        "year_built": submission.year_built,
    }
