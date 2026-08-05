import uuid
from django.db import models
from django.utils.text import slugify

from core.models import BaseModel, GeoLocationMixin


# =====================================================
# COUNTRY
# =====================================================
class Country(BaseModel):

    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        db_index=True,
    )

    name = models.CharField(max_length=100, unique=True)

    code = models.CharField(max_length=10, unique=True)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =====================================================
# STATE
# =====================================================
class State(BaseModel):

    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        db_index=True,
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="states",
    )

    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["country", "name"],
                name="unique_state_per_country",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.country.name}-{self.name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.country.name}"


# =====================================================
# LGA
# =====================================================
class LGA(BaseModel):

    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        db_index=True,
    )

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="lgas",
    )

    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "LGA"
        verbose_name_plural = "LGAs"
        constraints = [
            models.UniqueConstraint(
                fields=["state", "name"],
                name="unique_lga_per_state",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.state.name}-{self.name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.state.name}"


# =====================================================
# AREA
# =====================================================
class Area(GeoLocationMixin, BaseModel):

    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        db_index=True,
    )

    lga = models.ForeignKey(
        LGA,
        on_delete=models.PROTECT,
        related_name="areas",
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["lga", "name"],
                name="unique_area_per_lga",
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.lga.state.name}-{self.lga.name}-{self.name}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}, {self.lga.name}"