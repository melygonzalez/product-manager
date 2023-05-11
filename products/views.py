from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer, StaffProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'status', 'category']

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return StaffProductSerializer
        else:
            return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        if self.request.user.is_staff or self.request.user.is_superuser:
            category = self.request.query_params.get('category', None)
            if category is not None:
                queryset = queryset.filter(categories__name=category)
        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            serializer = StaffProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'You do not have permission to create products.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', True))
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to update products.'},
                            status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to retrieve this product.'},
                            status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_staff or request.user.is_superuser:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You do not have permission to delete this product.'},
                            status=status.HTTP_403_FORBIDDEN)
