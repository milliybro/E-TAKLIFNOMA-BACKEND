# Generated by Django 5.1.3 on 2024-11-18 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_invitation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('template_type', models.CharField(choices=[('horizontal', 'Gorizontal'), ('vertical', 'Vertikal'), ('animated', 'Animatsiyali')], max_length=20)),
                ('image', models.ImageField(upload_to='templates/')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
