# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from .serializers import UserSerializer

# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             User.objects.create_user(
#                 username=serializer.validated_data['username'],
#                 email=serializer.validated_data['email'],
#                 password=request.data['password']
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth.models import User
# from rest_framework.permissions import AllowAny

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         if not username or not email or not password:
#             return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
#         user = User.objects.create_user(username=username, email=email, password=password)
#         return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

# from rest_framework import generics
# from rest_framework.permissions import AllowAny
# from django.contrib.auth.models import User
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import UserSerializer

# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         email = request.data.get('email')
        
#         if User.objects.filter(username=username).exists():
#             return Response({"username": ["A user with that username already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        
#         if User.objects.filter(email=email).exists():
#             return Response({"email": ["A user with that email already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

import uuid
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            file_obj = request.data['file']
            logger.info(f"Received file: {file_obj.name}")

            filename = f"{uuid.uuid4()}_{timezone.now().strftime('%Y%m%d%H%M%S')}_{file_obj.name}"
            user_directory = os.path.join(settings.MEDIA_ROOT, 'uploads', str(request.user.id))
            os.makedirs(user_directory, exist_ok=True)
            file_path = os.path.join(user_directory, filename)

            with open(file_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            return Response({'filename': filename}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during file upload: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_directory = os.path.join(settings.MEDIA_ROOT, 'uploads', str(request.user.id))
        if not os.path.exists(user_directory):
            return Response([], status=status.HTTP_200_OK)
        
        files = os.listdir(user_directory)
        file_urls = [f"/media/uploads/{request.user.id}/{file}" for file in files]
        return Response(file_urls, status=status.HTTP_200_OK)

class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, filename, *args, **kwargs):
        user_directory = os.path.join(settings.MEDIA_ROOT, 'uploads', str(request.user.id))
        file_path = os.path.join(user_directory, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

