from django.forms import ModelForm
from .models import Record


class RecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['title',
                  'pub_date',
                  'start_date',
                  'end_date',
                  'milestone',
                  'description',
                  'type',
                  'participants',
                  'tags'
                  ]
