from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from central.base_model import BaseModel
from central.models import University

class Category(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):  # Show name as the identifying field
        return self.name


class Listing(BaseModel):
    realtor = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True)  # Optional description, no max length
    location = models.CharField(max_length=350)
    photo_main = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )  # Save inside media folder under date structure
    photo_1 = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )  # Optional extra photos
    photo_2 = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )
    photo_3 = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )
    photo_4 = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )
    photo_5 = models.ImageField(
        upload_to="listings/%Y/%m/%d/",
        blank=True,
        null=True,
        default="defaults/no-image.jpeg",
    )
    university = models.ForeignKey(University, on_delete=models.CASCADE , null=True)
    price = models.IntegerField(default=0)
    agent_fee = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0, null=False)
    new_house = models.BooleanField(default=False)
    gated_compound = models.BooleanField(default=False)
    running_water = models.BooleanField(default=False)
    generator = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # TODO
        self.slug = slugify(self.title)
        super(Listing, self).save(*args, **kwargs)

    def __str__(self):  # Show title as the identifier
        return "{} -> Realtor is {}  -> University is {}".format(
            self.title, self.realtor.username, self.university.name
        )


class listingRequest(BaseModel):
    email = models.EmailField(default=True)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)