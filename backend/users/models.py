from django.db import models
from django.contrib.auth.models import User
from central.models import University
from django.dispatch import receiver
from django.db.models.signals import post_save
from listings.models import Listing
from central.base_model import BaseModel

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    school = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(
        upload_to="profile_images/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/profile_default.jpeg",
    )
    models.URLField(
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    is_agent = models.BooleanField(default=False)
    completed_profile = models.BooleanField(default=False)
    

    def get_user_listings(self, *args, **kwargs):
        all_listings = Listing.objects.filter(realtor=self.user)
        return all_listings

    def get_user_listings_count(self, *args, **kwargs):
        all_listings_count = Listing.objects.filter(realtor=self.user).count()
        return all_listings_count

    def __str__(self):  # Show name as the identifying field
        return "{}'s Profile".format(self.user.username)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get("created", False):
        Profile.objects.get_or_create(user=kwargs.get("instance"))




class Verification(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_verification"
    )

    birth_date = models.CharField(max_length=20)
    guarantor_name = models.CharField(max_length=200)
    guarantor_address = models.CharField(max_length=200)
    guarantor_phone = models.CharField(max_length=20)
    id_num = models.CharField(max_length=20)
    id_card = models.ImageField(
        upload_to="IDcard/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/IDcard_default.jpeg",
    )
    models.URLField(
        blank=True,
        null=True,
    )

    size = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)
    


    def __str__(self):  # Show name as the identifying field
        return "{}'s verification info".format(self.user.username)