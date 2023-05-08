from rest_framework import serializers

from products.models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class StaffProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new Product, given the validated data.
        """
        categories_data = validated_data.pop('categories')
        images = validated_data.get('images')
        product = Product()
        product.name = validated_data.get('name')
        product.status = validated_data.get('status')
        product.save()
        for category in categories_data:
            current_category, created = Category.objects.get_or_create(name=category['name'])
            product.categories.add(current_category)
        for image in images:
            current_image = ProductImage()
            current_image.image = image['image']
            current_image.product = product
            current_image.save()
        return product

    def update(self, instance, validated_data):
        """
        Update and return an existing Product, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        categories_data = validated_data.get('categories', instance.status)
        instance.categories.clear()
        for category in categories_data:
            current_category, created = Category.objects.get_or_create(name=category['name'])
            instance.categories.add(current_category)
        images = validated_data.get('images', instance.images)
        ProductImage.objects.filter(product=instance.pk).delete()
        for image in images:
            current_image = ProductImage()
            current_image.image = image['image']
            current_image.product = instance
            current_image.save()
        instance.save()
        return instance

    def delete(self, instance):
        """
        Delete an existing Product.
        """
        return Product.objects.delete(instance)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'status']
