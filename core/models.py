from django.db import models
from django.utils import timezone 
from django.conf import settings
import uuid



# =====================================================
# GEO LOCATION MIXIN
# =====================================================
class GeoLocationMixin(models.Model):
    """
    Adds latitude and longitude to location-based models.

    Use this for:
    - Area
    - Property
    - Future service provider locations
    """
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


# =====================================================
# BASE MODEL
# =====================================================
class BaseModel(models.Model):
    """
    Base model for major Rentora entities.

    Provides:
    - uuid: public-safe identifier
    - created_at: creation timestamp
    - updated_at: update timestamp
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


# =====================================================
# SOFT ARCHIVE MIXIN
# =====================================================
class SoftArchiveMixin(models.Model):
    """
    Adds archive behaviour to models.

    We archive records instead of deleting them, especially for
    important business entities like Property, Booking, Wallet, etc.
    """

    is_archived = models.BooleanField(
        default=False,
        db_index=True,
    )

    archived_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(class)s_archived_records",
    )

    archive_reason = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def archive(self, *, archived_by=None, archive_reason=None):
        """
        Archive this record.
        """

        self.is_archived = True
        self.archived_at = timezone.now()
        self.archived_by = archived_by
        self.archive_reason = archive_reason

        self.save(
            update_fields=[
                "is_archived",
                "archived_at",
                "archived_by",
                "archive_reason",
                "updated_at",
            ]
        )

    def restore(self):
        """
        Restore an archived record.
        """

        self.is_archived = False
        self.archived_at = None
        self.archived_by = None
        self.archive_reason = None

        self.save(
            update_fields=[
                "is_archived",
                "archived_at",
                "archived_by",
                "archive_reason",
                "updated_at",
            ]
        )


