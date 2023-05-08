from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.serializers import UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_list(request):
    """
    List all users if is_admin, or create a new user.
    """
    if request.method == 'GET':
        if request.user.is_superuser:
            users = User.objects.all()
            serializer = UserSerializer(users, context={'request': request}, many=True)
            return Response(serializer.data)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def user_approval(request, pk):
    """
    Approve users if is_admin.
    """
    if request.method == 'PATCH':
        if request.user.is_superuser:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
