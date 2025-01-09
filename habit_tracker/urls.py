from django.urls import path
from django.views.generic import ArchiveIndexView

from habit_tracker.models import HabitCompletion

from . import views

app_name = "habit_tracker"
urlpatterns = [
    path("habits/", views.HabitListView.as_view(), name="habit_list"),
    path("habits/new/", views.HabitCreateView.as_view(), name="habit_create"),
    path("habits/<int:pk>/", views.HabitEditView.as_view(), name="habit_edit"),
    path('habits/<int:pk>/delete/', views.HabitDeleteView.as_view(), name='habit_delete'),
    path(
        "archive/",
        ArchiveIndexView.as_view(model=HabitCompletion, date_field="date"),
        name="archive",
    ),
    path(
        "<int:year>/<int:month>/<int:day>/",
        views.HabitCompletionDayArchiveView.as_view(month_format="%m"),
        name="archive_day",
    ),
    path("", views.TodayView.as_view(), name="today"),
]
