# Generated by Django 4.2.5 on 2023-09-05 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_gateway', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='card_number',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='order',
            name='cvv',
            field=models.CharField(max_length=3),
        ),
    ]