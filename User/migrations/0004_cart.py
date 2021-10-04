# Generated by Django 3.2.7 on 2021-10-02 05:06

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Enterprise', '0001_initial'),
        ('User', '0003_auto_20211001_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('product_items', djongo.models.fields.ArrayReferenceField(null=True, on_delete=djongo.models.fields.ArrayReferenceField._on_delete, to='Enterprise.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.users', verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Cart',
            },
        ),
    ]
