from django.contrib.auth.models import User, Permission
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'is_superuser', 'is_staff', 'user_permissions']

    def create(self, validated_data):
        """
        Create and return a new User, given the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing User, given the validated data.
        """
        change_permission = Permission.objects.get(
            codename="change_product",
        )
        delete_permission = Permission.objects.get(
            codename="delete_product",
        )
        instance.user_permissions.add(change_permission, delete_permission)
        instance.is_staff = True
        instance.save()
        return instance
