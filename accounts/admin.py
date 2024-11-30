from django.contrib import admin
from .models import User, Invitation, Template, FAQ, InvitationType, TemplateType

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_admin')

    def is_admin(self, obj):
        return obj.is_staff or obj.is_superuser  # yoki o'zingiz xohlagan shart
    is_admin.boolean = True  # Admin interfeysida haqiqiy/noto'g'ri belgisi ko'rsatiladi

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'groom_name', 'bride_name', 'wedding_time', 'wedding_date', 'venue_name')  # slugni ko'rsatish
    prepopulated_fields = {'slug': ('groom_name', 'bride_name')}  # slugni avtomatik to'ldirish



@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'description', 'image1', 'image2', 'image3', 'image4', 'image5')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')    

@admin.register(InvitationType)
class InvitationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Admin panelda ko'rinadigan ustunlar
    search_fields = ('name',)  # Qidiruv funksiyasi uchun maydon
    list_filter = ('name',)  # Filtrlash uchun maydon

    
@admin.register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # Admin ro'yxatida ko'rinadigan ustunlar
    search_fields = ('name',)  # Qidiruv uchun maydonlar
    list_filter = ('name',)  # Filtrlash uchun maydonlar