"""
URL configuration for education_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # 引入用於獲取 JWT 的視圖
    TokenRefreshView,     # 引入用於刷新 JWT 的視圖
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quizzes.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 用戶登錄後獲取訪問和刷新令牌的端點
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 使用刷新令牌來獲取新的訪問令牌的端點
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

