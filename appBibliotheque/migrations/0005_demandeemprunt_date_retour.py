# Generated by Django 5.0.3 on 2024-05-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBibliotheque', '0004_demandeemprunt'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandeemprunt',
            name='date_retour',
            field=models.DateField(blank=True, null=True),
        ),
    ]
