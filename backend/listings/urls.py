from .views import *
from django.urls import path


urlpatterns = [
    path('',getListings, name="listings"),
    path('categories', getCategories, name='categories'),

    path('create',createListing, name="listing-create"),
    path('upload',uploadImage, name="image-upload"),


    path('admin',getAdminListings, name='admin-listings'),
    path('<str:pk>',getListing, name="listing"),
    path('category/<str:pk>',getListingsByCategory, name="listings-category"),

    path('update/<str:pk>',updateListing, name="listing-update"),
    path('delete/<str:pk>',deleteListing, name="listing-delete"),


    
#     path('create/', createCategory, name="category-create"),

#     path('<str:pk>/', getCategory, name="category"),
#     path('update/<str:pk>/', updateCategory, name="category-update"),
#     path('delete/<str:pk>/', deleteCategory, name="category-delete"),
   
]