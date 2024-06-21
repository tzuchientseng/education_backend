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

from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        
        if User.objects.filter(username=username).exists():
            return Response({"username": ["A user with that username already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"email": ["A user with that email already exists."]}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
