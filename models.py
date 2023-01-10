import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Participant(models.Model):
    participant_name = models.CharField('Jméno', max_length=50)

    def __str__(self):
        return self.participant_name

    class Meta:
        verbose_name_plural = "Účastníci"


class Tag(models.Model):
    tag_title = models.CharField('Tag', max_length=30)

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name_plural = "Tagy"


class Type(models.Model):
    type_of_record = models.CharField(max_length=50)

    def __str__(self):
        return self.type_of_record

    class Meta:
        verbose_name_plural = "Typy"


class Record(models.Model):
    title = models.CharField('Název', max_length=150)
    pub_date = models.DateTimeField('Vloženo')
    start_date = models.DateField('Začátek')
    end_date = models.DateField('Konec')
    milestone = models.CharField('Milník', max_length=150)
    description = models.CharField('Popis', max_length=1000)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, verbose_name="Typ")
    participants = models.ManyToManyField(Participant, verbose_name="Účastníci")
    tags = models.ManyToManyField(Tag, verbose_name="Tagy")

    def __init__(self, *args, **kwargs):
        super(Record, self).__init__(*args, **kwargs)

    def __str__(self):

        return self.title

    class Meta:
        verbose_name_plural = "Záznamy"

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Publikováno nedávno?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now


