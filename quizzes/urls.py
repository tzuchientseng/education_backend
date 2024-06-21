# # quizzes/urls.py

# from django.urls import path
# from .views import RegisterView

# urlpatterns = [
#     path('auth/register/', RegisterView.as_view(), name='register'),
# ]
from django.urls import path
from .views import FileUploadView, FileListView, FileDeleteView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('delete/<str:filename>/', FileDeleteView.as_view(), name='file-delete'),
]
