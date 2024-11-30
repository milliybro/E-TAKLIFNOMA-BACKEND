from rest_framework import serializers
from .models import Invitation, Template, FAQ, InvitationType, TemplateType
from django.contrib.auth.models import User

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'template_type', 'image1', 'image2', 'image3', 'image4', 'image5']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class InvitationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationType
        fields = ['id', 'name', 'description']


class TemplateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateType
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User.groups.through  # Guruh modeli (standart)
        fields = ('id', 'name')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 
            'avatar', 'phone', 'position', 'is_active', 'date_joined', 
            'groups'
        )