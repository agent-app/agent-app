from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Listing, Category
from central.models import School
from .serializers import ListingSerializer, CategorySerializer


@api_view(['GET'])
def getListings(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    listings = Listing.objects.filter(
        title__icontains=query).order_by('-created_at')

    page = request.query_params.get('page')
    paginator = Paginator(listings, 10)

    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = ListingSerializer(listings, many=True)
    return Response({'listings': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getListingsByCategory(request, pk):
    category = Category.objects.get(id=pk)
    listings = category.listing_set.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def getTopListings(request):
#     listings = Listing.objects.filter(rating__gte=4).order_by('-rating')[0:7]
#     serializer = ListingSerializer(listings, many=True)
#     return Response(serializer.data)

@api_view(['GET'])

def getAdminListings(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getListing(request, pk):
    listing = Listing.objects.get(id=pk)
    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createListing(request):
    user = request.user
    data = request.data
    cat_id = data['category']
    category = Category.objects.get(id=cat_id)
    sch_id = data['school']
    school = School.objects.get(id=sch_id)

    listing = Listing.objects.create(
        realtor=user,
        title='',
        description='',
        location='',
        price=0,
        agent_fee=0,
        category=category,
        number_of_rooms=0,
        gated_compound=False,
        running_water=False,
        generator=False,
        new_house=False,
        state='',
        school=school
    )

    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateListing(request, pk):
    data = request.data
    listing = Listing.objects.get(id=pk)
    cat_id = data['category']
    category = Category.objects.get(id=cat_id)
    

    listing.title = data['title']
    listing.price = data['price']
    listing.description = data['description']
    listing.location = data['location']
    listing.category = category
    listing.agent_fee = data['agent_fee']
    listing.number_of_rooms = data['number_of_rooms']
    listing.gated_compound = data['gated_compound']
    listing.running_water = data['running_water']
    listing.generator = data['generator']
    listing.new_house = data['new_house']
    listing.state = data['state']
    listing.school = data['school']

    listing.save()

    serializer = ListingSerializer(listing, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteListing(request, pk):
    listing = Listing.objects.get(id=pk)
    listing.delete()
    return Response('listing Deleted')


@api_view(['POST'])
def uploadImage(request):
    data = request.data

    listingid = data['listingid']
    listing = Listing.objects.get(id=listingid)

    listing.image = request.FILES.get('image')
    listing.save()

    return Response('Image was uploaded')



@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getCategory(request, pk):
    category = Category.objects.get(id=pk)
    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCategory(request):
    user = request.user
    data = request.data

    category = Category.objects.create(
        user=user,
        name=data['name'],
    )

    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCategory(request, pk):
    data = request.data
    category = Category.objects.get(id=pk)

    category.name = data['name']

    category.save()

    serializer = CategorySerializer(category, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return Response('Category Deleted')