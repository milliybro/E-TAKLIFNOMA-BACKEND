from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import create_invitation, invitation_list_create, invitation_get
from accounts.views import InvitationListCreateAPIView, TemplateListCreateAPIView, TemplateDetailAPIView, FAQListCreateAPIView, invitation_type_detail, invitation_type_list_create, template_type_detail, template_type_list, UserProfileView

schema_view = get_schema_view(
    openapi.Info(
        title="E-TAKLIFNOMA API",
        default_version='v1',
        description="E-TAKLIFNOMA loyihasi uchun API hujjatlari",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/invitations/', InvitationListCreateAPIView.as_view(), name='invitation-list-create'),
    path('api/invitations/<int:pk>/', invitation_get, name='invitation-detail'),
    path('api/templates/', TemplateListCreateAPIView.as_view(), name='template-list-create'),
    path('api/templates/<int:pk>/', TemplateDetailAPIView.as_view(), name='template-detail'),
    path('api/faqs/', FAQListCreateAPIView.as_view(), name='faq-list-create'),
    path('api/invitation-types/', invitation_type_list_create, name='invitation_type_list_create'),
    path('api/invitation-types/<int:pk>/', invitation_type_detail, name='invitation_type_detail'),
    path('api/template-types/', template_type_list, name='template_type_list'),
    path('api/template-types/<str:name>/', template_type_detail, name='template_type_detail'),
    path('account/me/', UserProfileView.as_view(), name='user-profile'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
