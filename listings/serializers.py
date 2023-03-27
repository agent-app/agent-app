from rest_framework import serializers
from .models import Listing, Category


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    listings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_listings(self, obj):
        listings = obj.listing_set.all()
        serializer = ListingSerializer(listings, many=True)
        return serializer.data