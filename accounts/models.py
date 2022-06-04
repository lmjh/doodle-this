from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserAccount(models.Model):
    """
    A user account model for storing a user's address details, order history,
    and saved images.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_address_1 = models.CharField(max_length=80, null=True, blank=True)
    default_address_2 = models.CharField(max_length=80, null=True, blank=True)
    default_town = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=40, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_or_create_user_account(sender, created, instance, **kwargs):
    """
    When a post_save signal is received from the User model, create or update
    the corresponding user_account.
    """
    # if a User has been created, create a UserAccount
    if created:
        UserAccount.objects.create(user=instance)
    # otherwise just save the UserAccount
    instance.useraccount.save()
