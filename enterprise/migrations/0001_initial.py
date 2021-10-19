# Generated by Django 3.2.7 on 2021-10-19 05:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50, verbose_name='Category-Name')),
                ('category_image', models.ImageField(upload_to='Category', verbose_name='Category-Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('enterprise_name', models.CharField(max_length=50, verbose_name='Enterprise-Name')),
                ('enterprise_password', models.CharField(max_length=64, verbose_name='Password')),
                ('enterprise_email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('enterprise_photo', models.ImageField(upload_to='Enterprise/profile_photo', verbose_name='Profile-photo')),
                ('enterprise_contact', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{10}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Enterprises',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=50, verbose_name='Product-Name')),
                ('product_img', models.ImageField(upload_to='Product', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])], verbose_name='Product-image')),
                ('Price', models.PositiveIntegerField(verbose_name='price')),
                ('Description', models.TextField(verbose_name='Description')),
                ('product_qty', models.PositiveIntegerField(verbose_name='Product-quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('product_categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprise.categories', verbose_name='Product-Categories')),
                ('product_enterprsie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='enterprise.enterprise', verbose_name='Product-Enterprise')),
            ],
            options={
                'verbose_name_plural': 'Products',
            },
        ),
    ]
