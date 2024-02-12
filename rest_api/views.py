from django.shortcuts import render
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from accounts.backends import JWTAuthentication
from .serializers import CategorySerializer, TagsSerializer, TagMapSerializer, StocksSerializer, QuantitySerializer
from .models import Category, Tags, Stock, TagMap, Quantity

@swagger_auto_schema(
        method='post',
        operation_description="Create new Category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Category'],
    )
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_category(request):
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
        method='get',
        operation_description="get categories",
        tags=['Category'],
        security=[],
    )
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_categories(request):
    if request.method == 'GET':
        try:
            categories = Category.objects.all()
            if categories:
                serializer = CategorySerializer(categories, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    

@swagger_auto_schema(
        method='post',
        operation_description="Create new Stock",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['sku', 'name', 'price', 'category', 'allocated', 'alloc_build', 'alloc_sales', 'available', 'incoming', 'build_order', 'net_stock', 'tags'],
            properties={
                'sku': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                'category': openapi.Schema(type=openapi.TYPE_STRING),
                'allocated': openapi.Schema(type=openapi.TYPE_INTEGER),
                'alloc_build': openapi.Schema(type=openapi.TYPE_INTEGER),
                'alloc_sales': openapi.Schema(type=openapi.TYPE_INTEGER),
                'available': openapi.Schema(type=openapi.TYPE_INTEGER),
                'incoming': openapi.Schema(type=openapi.TYPE_INTEGER),
                'build_order': openapi.Schema(type=openapi.TYPE_INTEGER),
                'net_stock': openapi.Schema(type=openapi.TYPE_INTEGER),
                'instock': openapi.Schema(type=openapi.TYPE_INTEGER),
                'tags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING) )
            },
        ),
        security=[],
        tags=['Stocks'],
    )
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_stock(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cat = Category.objects.get(name=request.data.get('category'))
                stock = Stock(sku=request.data.get('sku'), name=request.data.get('name'), price=request.data.get('price'), category=cat)
                stock.save()
                sku = Stock.objects.get(sku=request.data.get('sku'))
                if request.data.get('net_stock') - request.data.get('alloc_build') > 0:
                    can_build = True
                else:
                    can_build = False
                quantity = Quantity(sku=sku, allocated=request.data.get('allocated'), alloc_build=request.data.get('alloc_build'), alloc_sales=request.data.get('alloc_sales'), available=request.data.get('available'), incoming=request.data.get('incoming'), build_order=request.data.get('build_order'), net_stock=request.data.get('net_stock'), can_build=can_build, instock=request.data.get('instock'))
                quantity.save()
                tags = request.data.get('tags')
                for t in tags:
                    tobj = Tags.objects.get(name=t)
                    tagMap = TagMap(tag=tobj, sku=sku)
                    tagMap.save()
            
            return Response({"message:": "Successfully created Stock entry"},status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response({"error:": "Unable to create stock"}, status=status.HTTP_400_BAD_REQUEST)



can_build = openapi.Parameter('can_build', in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)
category = openapi.Parameter('category', in_=openapi.IN_QUERY, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING) )
@swagger_auto_schema(
       method='get',
       manual_parameters=[can_build, category],
       security=[],
       tags=['Stocks']
    )
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_stock_dashboard(request):
    if request.method == 'GET':
        try:
            stocks = Stock.objects.prefetch_related('quantity_set','tagmap_set').all() 
            category = request.query_params.get('category')
            can_build = request.query_params.get('can_build')
            if stocks:
                res = []
                for s in stocks:
                    if category and len(category) > 0 and str(s.category.name) not in category:
                        continue
                    if can_build and not s.quantity_set.all()[0].can_build:
                        continue
                    tags = []
                    for t in s.tagmap_set.all():
                        if str(t.sku) == str(s.sku):
                            tags.append(t.tag.name)
                    json = {
                        "sku": s.sku,
                        "name": s.name,
                        "category": s.category.name,
                        "instock": s.quantity_set.all()[0].instock,
                        "available_stock": s.quantity_set.all()[0].available,
                        "tags": tags
                    }
                    res.append(json)
                if(len(res) > 0):
                    return Response(res, status=status.HTTP_201_CREATED)
                return Response({"error": "No Stocks"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "No Stocks"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
        method='post',
        operation_description="Create new Tag",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                },
        ),
        security=[],
        tags=['Tags'],
    )
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_tags(request):
    if request.method == 'POST':
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "Unable to retrieve stocks"}, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
       method='get',
       security=[],
       tags=['Tags']
    )
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_tags(request):
    if request.method == 'GET':
        try:
            tags = Tags.objects.all()
            if tags:
                serializer = TagsSerializer(tags, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)