# Generated by Django 4.1.3 on 2023-01-06 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_record', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Název')),
                ('pub_date', models.DateTimeField(verbose_name='Vloženo')),
                ('start_date', models.DateField(verbose_name='Začátek')),
                ('end_date', models.DateField(verbose_name='Konec')),
                ('milestone', models.CharField(max_length=150, verbose_name='Milník')),
                ('description', models.CharField(max_length=1000, verbose_name='Popis')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chronicle.type')),
            ],
        ),
    ]