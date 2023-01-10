from django.contrib import admin

from .models import Record, Type, Participant, Tag


class RecordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['title']}),
        ('Časové informace',  {'fields': ['pub_date', 'start_date', 'end_date']}),
        ('Textové informace', {'fields': ['milestone', 'description']}),
        ('Další informace',   {'fields': ['participants', 'tags', 'type']}),
    ]
    list_display = ('title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Record, RecordAdmin)
admin.site.register(Type)
admin.site.register(Participant)
admin.site.register(Tag)


