from django.urls import path

from . import views

app_name = "quotes"
urlpatterns = [
    path("", views.QuotesListView.as_view(), name="quotes_list"),
    path("new/", views.QuoteCreateView.as_view(), name="quote_create"),
    path("<int:pk>/", views.QuoteEditView.as_view(), name="quote_edit"),
    path("<int:pk>/delete", views.QuoteDeleteView.as_view(), name="quote_delete"),
]
