from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import WeeklyQuote


class QuotesListView(ListView):
    model = WeeklyQuote
    template_name = "quotes/quote_list.html"
    context_object_name = "quotes"


class QuoteCreateView(CreateView):
    model = WeeklyQuote
    fields = ["quote"]
    template_name = "quotes/quote_create.html"
    success_url = reverse_lazy("quotes:quotes_list")


class QuoteEditView(UpdateView):
    model = WeeklyQuote
    fields = ["quote"]
    template_name = "quotes/quote_edit.html"
    success_url = reverse_lazy("quotes:quotes_list")


class QuoteDeleteView(DeleteView):
    model = WeeklyQuote
    template_name = "quotes/quote_delete.html"
    success_url = reverse_lazy("quotes:quotes_list")
