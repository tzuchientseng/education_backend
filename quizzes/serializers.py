from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Meta 類用於指定序列化器的設置
    class Meta:
        model = User  # 指定對應的模型為 User
        fields = ['id', 'username', 'email', 'password']  # 指定要序列化的字段
        extra_kwargs = {'password': {'write_only': True}}  # 設置密碼字段為只寫，不在響應中顯示

    def create(self, validated_data):
        # 重寫 create 方法，以便在創建 User 時使用 create_user 方法
        user = User.objects.create_user(
            username=validated_data['username'],  # 從驗證數據中獲取 username
            email=validated_data['email'],  # 從驗證數據中獲取 email
            password=validated_data['password']  # 從驗證數據中獲取 password，並哈希處理
        )
        return user  # 返回創建的 User 實例
