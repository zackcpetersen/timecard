from rest_framework import serializers
from accounts.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()

    def get_full_name(self, user):
        return '{} {}'.format(user.first_name, user.last_name)

    def get_initials(self, user):
        return '{}{}'.format(user.first_name[0], user.last_name[0])


class UserCreationSerializer(UserBaseSerializer):
    image = serializers.ImageField(read_only=True)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'initials', 'full_name',
                  'email', 'is_admin', 'is_superuser', 'image', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(UserBaseSerializer):
    is_admin = serializers.BooleanField(read_only=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'initials', 'full_name',
                  'email', 'is_admin', 'is_superuser', 'image', 'pass_valid']
