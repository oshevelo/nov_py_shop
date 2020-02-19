from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
    	many=True,
        slug_field='codename',
        queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')

'''class UserRegisterSerializer(serializers.ModelSerializer):
	token = serializers.SerializerMethodField(‘get_user_token’)
	def get_user_token(self, obj):
		token, created = Token.objects.get_or_create(user=obj.user)
		return token.key
	class Meta:
		model = User'''