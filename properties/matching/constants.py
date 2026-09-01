"""
Configuration for the property duplicate-matching engine.

This file contains matching rules and configuration only.
It should not contain database queries or business logic.
"""


# ============================================================
# MATCH DECISION THRESHOLDS
# ============================================================

# Normal property categories:
#
# 85+  -> automatically considered a duplicate
# 65-84 -> requires admin review
# <65 -> not considered a duplicate

DEFAULT_AUTO_MATCH_THRESHOLD = 85
DEFAULT_ADMIN_REVIEW_THRESHOLD = 65


# Land requires a higher confidence level because
# land listings can cover large areas and may have
# fewer distinguishing physical characteristics.

LAND_AUTO_MATCH_THRESHOLD = 90
LAND_ADMIN_REVIEW_THRESHOLD = 70


# ============================================================
# PROPERTY CATEGORIES
# ============================================================

HOUSE = "house"
APARTMENT = "apartment"
ESTATE = "estate"
ROOM = "room"
COMMERCIAL = "commercial"
LAND = "land"


PROPERTY_CATEGORIES = (
    HOUSE,
    APARTMENT,
    ESTATE,
    ROOM,
    COMMERCIAL,
    LAND,
)


# ============================================================
# MATCH DECISIONS
# ============================================================

AUTO_MATCH = "auto_match"
ADMIN_REVIEW = "admin_review"
NOT_DUPLICATE = "not_duplicate"


MATCH_DECISIONS = (
    AUTO_MATCH,
    ADMIN_REVIEW,
    NOT_DUPLICATE,
)


# ============================================================
# MATCHING WEIGHTS
# ============================================================

"""
Each category has its own scoring matrix.

The values represent the maximum contribution of
each matching characteristic to the overall score.

The total weight for each matrix is 100.
"""


# ------------------------------------------------------------
# STANDALONE HOUSE / DUPLEX
# ------------------------------------------------------------

HOUSE_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "bedrooms": 10,
    "bathrooms": 5,
    "address": 15,
    "landmark": 5,
    "location": 20,
}


# ------------------------------------------------------------
# APARTMENT / FLAT
# ------------------------------------------------------------

APARTMENT_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "bedrooms": 10,
    "bathrooms": 5,
    "address": 15,
    "landmark": 5,
    "location": 20,
}


# ------------------------------------------------------------
# ESTATE PROPERTY
# ------------------------------------------------------------

ESTATE_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "bedrooms": 5,
    "bathrooms": 5,
    "address": 15,
    "landmark": 10,
    "location": 20,
}


# ------------------------------------------------------------
# ROOM
# ------------------------------------------------------------

ROOM_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "bedrooms": 10,
    "bathrooms": 10,
    "address": 15,
    "landmark": 5,
    "location": 15,
}


# ------------------------------------------------------------
# COMMERCIAL PROPERTY
# ------------------------------------------------------------

COMMERCIAL_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "address": 20,
    "landmark": 10,
    "location": 25,
}


# ------------------------------------------------------------
# LAND
# ------------------------------------------------------------

LAND_WEIGHTS = {
    "area": 20,
    "property_type": 15,
    "purpose": 10,
    "address": 15,
    "landmark": 10,
    "location": 30,
}


# ============================================================
# CATEGORY -> WEIGHT MATRIX
# ============================================================

CATEGORY_WEIGHTS = {
    HOUSE: HOUSE_WEIGHTS,
    APARTMENT: APARTMENT_WEIGHTS,
    ESTATE: ESTATE_WEIGHTS,
    ROOM: ROOM_WEIGHTS,
    COMMERCIAL: COMMERCIAL_WEIGHTS,
    LAND: LAND_WEIGHTS,
}


# ============================================================
# CATEGORY -> THRESHOLDS
# ============================================================

CATEGORY_THRESHOLDS = {
    HOUSE: {
        "auto_match": DEFAULT_AUTO_MATCH_THRESHOLD,
        "admin_review": DEFAULT_ADMIN_REVIEW_THRESHOLD,
    },
    APARTMENT: {
        "auto_match": DEFAULT_AUTO_MATCH_THRESHOLD,
        "admin_review": DEFAULT_ADMIN_REVIEW_THRESHOLD,
    },
    ESTATE: {
        "auto_match": DEFAULT_AUTO_MATCH_THRESHOLD,
        "admin_review": DEFAULT_ADMIN_REVIEW_THRESHOLD,
    },
    ROOM: {
        "auto_match": DEFAULT_AUTO_MATCH_THRESHOLD,
        "admin_review": DEFAULT_ADMIN_REVIEW_THRESHOLD,
    },
    COMMERCIAL: {
        "auto_match": DEFAULT_AUTO_MATCH_THRESHOLD,
        "admin_review": DEFAULT_ADMIN_REVIEW_THRESHOLD,
    },
    LAND: {
        "auto_match": LAND_AUTO_MATCH_THRESHOLD,
        "admin_review": LAND_ADMIN_REVIEW_THRESHOLD,
    },
}