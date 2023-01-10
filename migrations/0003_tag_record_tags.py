# Generated by Django 4.1.3 on 2023-01-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chronicle', '0002_participant_record_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_title', models.CharField(max_length=30, verbose_name='Tag')),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='tags',
            field=models.ManyToManyField(to='chronicle.tag'),
        ),
    ]
