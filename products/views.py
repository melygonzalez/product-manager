from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer, StaffProductSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def product_list(request):
    """
    List all products, or create a new product.
    """
    if request.method == 'GET':
        product_name = request.query_params.get('name')
        product_status = request.query_params.get('status')
        products = Product.objects.all()
        if product_name:
            products = products.filter(name=product_name)
        if product_status:
            products = products.filter(status=product_status)
        if request.user.is_authenticated:
            product_category = request.query_params.get('category')
            if product_category:
                products = products.filter(categories__name=product_category)
            serializer = StaffProductSerializer(products, context={'request': request}, many=True)
            return Response(serializer.data)
        serializer = ProductSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user.is_staff or request.user.is_superuser:
            serializer = StaffProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a product.
    """
    if not request.user.is_staff or not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StaffProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = StaffProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

