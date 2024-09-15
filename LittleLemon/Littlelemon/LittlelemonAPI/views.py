from rest_framework import generics
from .models import MenuItem, Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MenuItemSerializer , MenuCategorySerailizer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import EmptyPage , Paginator

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import permission_classes , throttle_classes, authentication_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsThrottles

# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItem.objects.select_related('category').all()
#     serializer_class = MenuItemSerializer

# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


# class MenuCategoryView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = MenuCategorySerailizer

# class SingleMenuCategory(generics.RetrieveUpdateAPIView , generics.DestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = MenuCategorySerailizer



@api_view(['GET' , 'POST'])
def menuitems(request):
    if (request.method == 'GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        page = request.query_params.get('page' , default=1)
        perpage = request.query_params.get('perpage', default=2)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__contains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        paginator = Paginator(items, per_page=perpage)

        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_Data = MenuItemSerializer(items, many=True)
        return Response(serialized_Data.data)
    if(request.method == 'POST'):
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data , status.HTTP_201_CREATED)
        

# @api_view()
# def singleItem(request, pk):
#     item = get_object_or_404(MenuItem , id=pk)
#     serialized_Data = MenuItemSerializer(item)
#     return Response(serialized_Data.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def secret(request):
    return Response({'message' : "This is Secret Message"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def managerview(request):
    if request.user.groups.filter(name='Admin').exists():
        return Response({"mesasge" : "Only Manager"})
    else:
        return Response({'message' : "You are not authorized"})
    

@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def throttle(request):
    return Response({'Message': "This is Accessible"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsThrottles])
def loggedusers(request):
    return Response({'message' : "Only Logged Users"})