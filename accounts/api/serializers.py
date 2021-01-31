from rest_framework import serializers
from accounts.models import User


class UserCreationSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_admin',
                  'is_superuser', 'last_login', 'is_active', 'is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    initials = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'initials', 'full_name',
                  'email', 'is_admin', 'is_superuser', 'image']

    def get_initials(self, user):
        return '{}{}'.format(user.first_name[0], user.last_name[0])

    def get_full_name(self, user):
        return '{} {}'.format(user.first_name, user.last_name)
