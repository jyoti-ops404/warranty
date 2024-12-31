from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Vendor

# Add vendor automatically when created new user with user full name as vendor name
@receiver(post_save, sender=User)
def create_or_update_vendor(sender, instance, created, **kwargs):
    # Check if the user has both first_name and last_name
    if instance.first_name or instance.last_name:
        full_name = f"{instance.first_name} {instance.last_name}".strip()

        # Create or update the Vendor entry
        Vendor.objects.update_or_create(user=instance, defaults={"name": full_name})