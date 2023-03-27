from rest_framework import serializers
from authentication.models import User, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['size', 'verified']
    
    def validate_file(self, value):
        # Validate the file size
        if value.size > 1024*1024:  # 1 MB
            raise serializers.ValidationError('File size exceeds 1 MB')
        # Validate the file type
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError('Only PDF files are allowed')
        return value


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.full_name
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'