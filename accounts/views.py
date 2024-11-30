from django.contrib.auth import authenticate, login
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Invitation, Template, FAQ, InvitationType, TemplateType
from .serializers import InvitationSerializer, TemplateSerializer, FAQSerializer, InvitationTypeSerializer, TemplateTypeSerializer, UserProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from django.views.generic import DetailView
from rest_framework.permissions import IsAuthenticated
import random

@csrf_exempt
def login_or_register(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        user, created = User.objects.get_or_create(phone_number=phone)
        password = str(random.randint(1000, 9999))

        if not created and user.check_password(password):
            return JsonResponse({'error': 'Oldingi parolni ishlatishingiz mumkin emas'}, status=400)

        user.set_password(password)
        user.save()

        # TODO: Parolni Telegram botiga yuboring
        # Telegram botga parolni yuborish uchun kerakli API integratsiyasini bu yerda bajaring.

        return JsonResponse({'message': 'Parol yuborildi'}, status=200)

def create_invitation(request):
    serializer = InvitationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Taklifnomalar ro'yxati va yaratish
@api_view(['GET', 'POST'])
def invitation_list_create(request):
    if request.method == 'GET':
        invitations = Invitation.objects.all()
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Taklifnomani ko'rish, yangilash va o'chirish
@api_view(['GET', 'PUT', 'DELETE'])
def invitation_get(request, pk):
    try:
        invitation = Invitation.objects.get(pk=pk)
    except Invitation.DoesNotExist:
        return Response({"error": "Taklifnoma topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvitationSerializer(invitation)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = InvitationSerializer(invitation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        invitation.delete()
        return Response({"message": "Taklifnoma o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


class InvitationListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Barcha taklifnomalarni olish",
        responses={200: InvitationSerializer(many=True)}
    )
    def get(self, request):
        invitations = Invitation.objects.all()
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yangi taklifnoma yaratish",
        request_body=InvitationSerializer,
        responses={201: InvitationSerializer}
    )
    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Barcha shablonlarni olish",
        responses={200: TemplateSerializer(many=True)}
    )
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yangi shablon yaratish",
        request_body=TemplateSerializer,
        responses={201: TemplateSerializer}
    )
    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Shablonni ID bo‘yicha olish",
        responses={200: TemplateSerializer}
    )
    def get(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Shablon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Shablonni yangilash",
        request_body=TemplateSerializer,
        responses={200: TemplateSerializer}
    )
    def put(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Shablon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Shablonni o'chirish",
        responses={204: "Shablon o'chirildi"}
    )
    def delete(self, request, pk):
        try:
            template = Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            return Response({"error": "Shablon topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        template.delete()
        return Response({"message": "Shablon o'chirildi"}, status=status.HTTP_204_NO_CONTENT)
    

class FAQListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Barcha savollar va javoblarni olish",
        responses={200: FAQSerializer(many=True)}
    )
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yangi savol va javob qo'shish",
        request_body=FAQSerializer,
        responses={201: FAQSerializer}
    )
    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def invitation_detail(request, slug):
    try:
        invitation = Invitation.objects.get(slug=slug)
    except Invitation.DoesNotExist:
        raise Http404("Invitation not found")

    return render(request, 'invitation_detail.html', {'invitation': invitation})


class InvitationDetailView(DetailView):
    model = Invitation
    template_name = 'invitation_detail.html'
    context_object_name = 'invitation'


@api_view(['GET', 'POST'])
def invitation_type_list_create(request):
    if request.method == 'GET':
        types = InvitationType.objects.all()
        serializer = InvitationTypeSerializer(types, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = InvitationTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def invitation_type_detail(request, pk):
    try:
        invitation_type = InvitationType.objects.get(pk=pk)
    except InvitationType.DoesNotExist:
        return Response({"error": "Taklifnoma turi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvitationTypeSerializer(invitation_type)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = InvitationTypeSerializer(invitation_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        invitation_type.delete()
        return Response({"message": "Taklifnoma turi o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


class InvitationTypeListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Barcha taklifnoma turlarini olish",
        responses={200: InvitationTypeSerializer(many=True)}
    )
    def get(self, request):
        types = InvitationType.objects.all()
        serializer = InvitationTypeSerializer(types, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Yangi taklifnoma turi qo'shish",
        request_body=InvitationTypeSerializer,
        responses={201: InvitationTypeSerializer}
    )
    def post(self, request):
        serializer = InvitationTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def template_type_list(request):
    """
    Barcha shablon turlarini qaytaruvchi API.
    """
    template_types = TemplateType.objects.all()
    serializer = TemplateTypeSerializer(template_types, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def template_type_detail(request, name):
    """
    Berilgan shablon turini qaytaruvchi API.
    """
    try:
        template_type = TemplateType.objects.get(name__iexact=name)
    except TemplateType.DoesNotExist:
        return Response({"error": "Shablon turi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TemplateTypeSerializer(template_type)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "User is not authenticated."}, status=403)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
