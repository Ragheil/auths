from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from .models import Profile
from .serializers import ProfileSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def register_api(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(user.email, auth_token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response("Login Successful", status=status.HTTP_200_OK)
        else:
            return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def profile_detail_api(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)