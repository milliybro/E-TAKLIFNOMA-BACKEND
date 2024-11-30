from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Telefon raqami kiritilishi kerak')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    
class Template(models.Model):
    TEMPLATE_CHOICES = [
        ('horizontal', 'Horizontal'),
        ('vertical', 'Vertical'),
        ('animated', 'Animated'),
    ]
    
    name = models.CharField(max_length=50)
    image1 = models.ImageField(upload_to='templates/', blank=True, null=True)
    image2 = models.ImageField(upload_to='templates/', blank=True, null=True)
    image3 = models.ImageField(upload_to='templates/', blank=True, null=True)
    image4 = models.ImageField(upload_to='templates/', blank=True, null=True)
    image5 = models.ImageField(upload_to='templates/', blank=True, null=True)
    description = models.TextField()
    template_type = models.CharField(max_length=10, choices=TEMPLATE_CHOICES)
    
    def __str__(self):
        return self.name


class Invitation(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    groom_name = models.CharField(max_length=255)
    bride_name = models.CharField(max_length=255)
    wedding_date = models.DateTimeField()
    organizers = models.CharField(max_length=255)
    venue_name = models.CharField(max_length=255)
    venue_address = models.TextField()
    venue_location = models.JSONField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='invitations', default=1)
    
    @property
    def wedding_time(self):
        return self.wedding_date.strftime('%H:%M')  # Faqat vaqtni qaytarish

    def __str__(self):
        return f"Invitation for {self.groom_name} and {self.bride_name}"
   

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
    
class InvitationType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class TemplateType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
