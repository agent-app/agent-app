from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from central.base_model import BaseModel
from central.constants import STATE_CHOICES

User = get_user_model()



class Category(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # TODO
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):  # Show name as the identifying field
        return self.name


class Listing(BaseModel):
    realtor = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    title = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(blank=True)  # Optional description, no max length
    location = models.CharField(max_length=35)
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
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default=None)
    school = models.ForeignKey("central.School", on_delete=models.CASCADE)  
    price = models.IntegerField(default=0)
    agent_fee = models.IntegerField(default=0)
    number_of_rooms = models.IntegerField(default=0, null=False)
    new_house = models.BooleanField(default=False)
    gated_compound = models.BooleanField(default=False)
    running_water = models.BooleanField(default=False)
    generator = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # TODO
        self.slug = slugify(self.title)
        super(Listing, self).save(*args, **kwargs)

    def __str__(self):  # Show title as the identifier
        return "{} --> Realtor : {} ".format(
            self.title, self.realtor.username
        )


class listingRequest(BaseModel):
    email = models.EmailField(default=True)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)