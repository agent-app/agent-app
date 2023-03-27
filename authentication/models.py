from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django.db.models.signals import post_save
import listings.models



class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
)



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    full_name = models.CharField(max_length=255, blank=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    gender = models.CharField(max_length=10, choices=GENDER, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    birth_date = models.CharField(max_length=20)
    profile_pic = models.ImageField(
        upload_to="profile_images/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/profile_default.jpeg",
    )
    phone_no = models.CharField(max_length=20)
    id_num = models.CharField(max_length=20)
    id_card = models.ImageField(
        upload_to="IDcard/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/IDcard_default.jpeg",
    )
    occupation = models.CharField(max_length=30, null=True)
    school = models.ForeignKey("central.School", on_delete=models.CASCADE, null=True)
    is_completed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_user_listings(self, *args, **kwargs):
        all_listings = listings.models.Listing.objects.filter(realtor=self.user)
        return all_listings

    def get_user_listings_count(self, *args, **kwargs):
        all_listings_count = listings.models.Listing.objects.filter(realtor=self.user).count()
        return all_listings_count

    def __str__(self):  # Show name as the identifying field
        return "{}'s Profile".format(self.user.username)


@receiver(post_save, sender=User)
def ensure_profile_exists(sender, **kwargs):
    if kwargs.get("created", False):
        UserProfile.objects.get_or_create(user=kwargs.get("instance"))