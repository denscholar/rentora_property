# ==========================================
# ACCOUNT SIGNALS
# ==========================================

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, UserProfile, AgentProfile, LandlordProfile


# ==========================================
# CREATE USER RELATED PROFILES
# ==========================================
@receiver(post_save, sender=CustomUser)
def create_user_related_profiles(sender, instance, created, **kwargs):
    if not created:
        return

    UserProfile.objects.get_or_create(user=instance)

    if instance.role == CustomUser.Role.AGENT:
        AgentProfile.objects.get_or_create(user=instance)

    if instance.role == CustomUser.Role.LANDLORD:
        LandlordProfile.objects.get_or_create(user=instance)