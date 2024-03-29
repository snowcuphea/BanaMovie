from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from movies.models import UserGenre

@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        temp_user = get_user_model().objects.get(pk=user.id)
        usergenre = UserGenre(
            user=temp_user
        )
        usergenre.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def is_admin(request):
    # print(request.data)
    user = get_user_model().objects.get(username=request.data["username"])
    # user = request.user
    if user.is_superuser : 
        # print("hello admin!")
        return Response(True, status=status.HTTP_202_ACCEPTED)
    else : 
        # print("not admin....")
        return Response(False)


@api_view(['POST'])
def manage_members(request):
    manager = get_user_model().objects.get(username=request.data['username'])
    if manager.is_superuser : 
        members = get_user_model().objects.all()
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)
    return Response(False)


@api_view(['POST'])
def delete_members(request, member_id):
    manager = get_user_model().objects.get(username=request.data['username'])
    if manager.is_superuser :
        member = get_user_model().objects.get(pk=member_id)
        member.delete()
        return Response({'who': member_id})
    return Response(False)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    return Response(request.user.id)