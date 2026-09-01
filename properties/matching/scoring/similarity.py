from decimal import Decimal, ROUND_HALF_UP

# ============================================================
# CONSTANTS
# ============================================================

ZERO = Decimal("0")
HUNDRED = Decimal("100")


# ============================================================
# HELPERS
# ============================================================


def decimal(value) -> Decimal:
    """
    Safely convert a value into Decimal.
    """

    if value is None:
        return ZERO

    return Decimal(str(value))


def clamp(
    value: Decimal,
    minimum: Decimal = ZERO,
    maximum: Decimal = HUNDRED,
) -> Decimal:
    """
    Keep a value inside a defined range.

    Example:

        -10  -> 0
         50  -> 50
        120  -> 100
    """

    return max(
        minimum,
        min(value, maximum),
    )


# ============================================================
# BOOLEAN SIMILARITY
# ============================================================


def boolean_similarity(value: bool) -> Decimal:
    """
    Convert a boolean match into a similarity percentage.

    True  -> 100
    False -> 0
    """

    return HUNDRED if value else ZERO


# ============================================================
# PERCENTAGE DIFFERENCE
# ============================================================


def percentage_difference_similarity(
    difference,
) -> Decimal:
    """
    Convert a percentage difference into similarity.

    Example:

        0% difference   -> 100% similarity
        10% difference  -> 90% similarity
        35% difference  -> 65% similarity
        100% difference -> 0% similarity

    Values above 100% are capped at 0 similarity.
    """

    if difference is None:
        return ZERO

    difference = decimal(difference)

    return clamp(
        HUNDRED - difference,
    )


# ============================================================
# NUMERIC DIFFERENCE
# ============================================================


def numeric_difference_similarity(
    difference,
    *,
    perfect_difference: int = 0,
    maximum_difference: int = 2,
) -> Decimal:
    """
    Convert an absolute numeric difference into similarity.

    Example with maximum_difference=2:

        difference = 0 -> 100
        difference = 1 -> 50
        difference = 2 -> 0
        difference > 2 -> 0
    """

    if difference is None:
        return ZERO

    difference = decimal(difference)
    perfect_difference = decimal(perfect_difference)
    maximum_difference = decimal(maximum_difference)

    if difference <= perfect_difference:
        return HUNDRED

    if difference >= maximum_difference:
        return ZERO

    usable_range = maximum_difference - perfect_difference

    distance_from_perfect = difference - perfect_difference

    similarity = HUNDRED * (usable_range - distance_from_perfect) / usable_range

    return clamp(similarity)


# ============================================================
# STRING SIMILARITY
# ============================================================


def string_similarity(
    similarity_percentage,
) -> Decimal:
    """
    Normalize an existing string similarity percentage.

    signals.py already produces values between 0 and 100,
    so this function mainly validates and normalizes them.
    """

    if similarity_percentage is None:
        return ZERO

    return clamp(
        decimal(similarity_percentage),
    )


# ============================================================
# CONTRIBUTION
# ============================================================


def weighted_contribution(
    similarity: Decimal,
    weight: Decimal,
) -> Decimal:
    """
    Calculate how much a signal contributes to the
    overall match score.

    Formula:

        contribution = similarity × weight / 100

    Example:

        similarity = 80
        weight = 20

        contribution = 16
    """

    similarity = clamp(
        decimal(similarity),
    )

    weight = decimal(weight)

    return (similarity * weight / HUNDRED).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
