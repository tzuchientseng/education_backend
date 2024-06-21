# # quizzes/urls.py

# from django.urls import path
# from .views import RegisterView

# urlpatterns = [
#     path('auth/register/', RegisterView.as_view(), name='register'),
# ]
from django.urls import path
from .views import UserCreate

urlpatterns = [
    path('auth/register/', UserCreate.as_view(), name='user-create'),
]
