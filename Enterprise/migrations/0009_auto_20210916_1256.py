# Generated by Django 3.2.7 on 2021-09-16 12:56

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('Enterprise', '0008_alter_products_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enterprise_detail',
            name='enterprise_categories',
        ),
        migrations.AddField(
            model_name='categories',
            name='enterprise_list',
            field=models.ManyToManyField(default='', to='Enterprise.Enterprise_Detail', verbose_name='Enterprise-list'),
        ),
        migrations.RemoveField(
            model_name='products',
            name='product_category',
        ),
        migrations.AddField(
            model_name='products',
            name='product_category',
            field=smart_selects.db_fields.ChainedManyToManyField(chained_field='product_enterprise', chained_model_field='enterprise_list', to='Enterprise.Categories', verbose_name='Product-Categories'),
        ),
    ]
