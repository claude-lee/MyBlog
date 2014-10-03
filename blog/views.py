from django.views.generic import DetailView
from .models import Entry


class EntryDetail(DetailView):
    model = Entry

entry_detail = EntryDetail.as_view()

