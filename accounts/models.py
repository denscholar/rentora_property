from django.db import models
import secrets
import uuid
import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django.contrib.auth.models import BaseUserManager

from accounts.constants import EMAIL_OTP_EXPIRY_MINUTES


# ==========================================
# CUSTOM USER MANAGER
# ==========================================
class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


# ==========================================
# CUSTOM USER
# ==========================================
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        TENANT = "tenant", "Tenant"
        AGENT = "agent", "Agent"
        LANDLORD = "landlord", "Landlord"
        ADMIN = "admin", "Admin"

    class AdminType(models.TextChoices):
        SUPER_ADMIN = (
            "super_admin",
            "Super Admin",
        )
        PROPERTY_MODERATOR = (
            "property_moderator",
            "Property Moderator",
        )
        FINANCE_ADMIN = (
            "finance_admin",
            "Finance Admin",
        )
        SUPPORT_ADMIN = (
            "support_admin",
            "Support Admin",
        )
        OPERATIONS_ADMIN = (
            "operations_admin",
            "Operations Admin",
        )

    slug = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    username = None

    email = models.EmailField(
        unique=True,
        db_index=True,
    )
    email_otp = models.CharField(
        max_length=6,
        blank=True,
        null=True,
    )

    email_otp_expires_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    admin_type = models.CharField(
        max_length=40,
        choices=AdminType.choices,
        blank=True,
        null=True,
        db_index=True,
    )

    email_otp_verified_at = models.DateTimeField(
        blank=True,
        null=True,
    )
    otp_created_at = models.DateTimeField(blank=True, null=True)
    last_otp_sent_at = models.DateTimeField(null=True, blank=True)

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    is_verified = models.BooleanField(default=False)

    email_verified_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "role",
    ]
    objects = CustomUserManager()

    class Meta:
        ordering = ["-created_at"]

    # ==========================================
    # GENERATE EMAIL OTP
    # ==========================================
    def generate_email_otp(self):
        # otp = str(random.randint(100000, 999999))
        otp = str(secrets.randbelow(900000) + 100000)

        self.email_otp = otp
        self.email_otp_expires_at = timezone.now() + timedelta(
            minutes=EMAIL_OTP_EXPIRY_MINUTES
        )
        self.save(
            update_fields=[
                "email_otp",
                "email_otp_expires_at",
                "updated_at",
            ]
        )

        return otp

    def clean(self):
        super().clean()

        if self.role == self.Role.ADMIN:
            if not self.admin_type:
                raise ValidationError(
                    {"admin_type": ("Admin users must have an admin type.")}
                )

        elif self.admin_type:
            raise ValidationError(
                {
                    "admin_type": (
                        "Only users with the admin role can have " "an admin type."
                    )
                }
            )

    def has_admin_permission(self, permission_code):
        if self.role != self.Role.ADMIN:
            return False

        if not self.admin_type:
            return False

        from accounts.admin_permissions import ADMIN_PERMISSIONS

        permissions = ADMIN_PERMISSIONS.get(
            self.admin_type,
            set(),
        )

        return permission_code in permissions

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


# ==========================================
# USER PROFILE
# ==========================================
class UserProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=100,
        default="Nigeria",
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True,
        null=True,
    )

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} Profile"


# ==========================================
# AGENT PROFILE
# ==========================================
class AgentProfile(models.Model):
    class VerificationStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="agent_profile",
    )

    agency_name = models.CharField(max_length=150, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)

    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_STARTED,
    )

    rating_average = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
    )

    completed_viewings = models.PositiveIntegerField(default=0)
    cancelled_viewings = models.PositiveIntegerField(default=0)
    no_show_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.get_full_name()} Agent Profile"


# ==========================================
# LANDLORD PROFILE
# ==========================================
class LandlordProfile(models.Model):
    class LandlordType(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        COMPANY = "company", "Company"
        ESTATE_COMPANY = "estate_company", "Estate Company"
        PROPERTY_MANAGER = "property_manager", "Property Manager"

    class VerificationStatus(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="landlord_profile",
    )

    landlord_type = models.CharField(
        max_length=30,
        choices=LandlordType.choices,
        default=LandlordType.INDIVIDUAL,
    )

    business_name = models.CharField(max_length=150, blank=True, null=True)

    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_STARTED,
    )

    total_properties = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.get_full_name()} Landlord Profile"
