import uuid
from django.db import models
from django.utils.text import slugify


# =====================================================
# LOOKUP BASE MODEL
# =====================================================
class LookupBaseModel(models.Model):

    """
    Shared foundation for configurable property lookup values.
    Lookup records are generally managed by administrators and exposed
    through read-only public API endpoints.
    
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    slug = models.SlugField(
        max_length=150,
        unique=True,
        editable=False,
        db_index=True,
    )

    description = models.TextField(blank=True)

    display_order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            generated_slug = slugify(self.name)
            self.slug = generated_slug or str(self.uuid)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
