from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

from .models import Record, Type, Participant, Tag
from .forms import RecordForm


class IndexView(generic.ListView):
    template_name = 'chronicle/index.html'
    context_object_name = 'latest_record_list'

    def get_queryset(self):
        """
        Return the last five published records (not including those set to be published in the future.
        """
        return Record.objects.filter(pub_date__lte=timezone.now()
                                     ).order_by('-pub_date')[:50]


class DetailView(generic.DetailView):
    model = Record
    template_name = 'chronicle/detail.html'

    def get_queryset(self):
        """
        Excludes any records that aren't published yet.
        """
        return Record.objects.filter(pub_date__lte=timezone.now())


class CreateRecord(generic.edit.CreateView):
    form_class = RecordForm
    template_name = 'chronicle/create.html'

    def get(self, request):
        """
        Method pictures only the form.
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Method checks the form, in case of valid data creates new record, in case of not valid data pictures error msg.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
        return render(request, self.template_name, {'form': form})
