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
        "<int:year>/<int:month>/<int:day>/",
        views.day_view,
        name="day_view",
    ),
    path(
        "today",
        views.redirect_today,
        name="redirect_today",
    ),
    path("", views.heatmap_view, name="heatmap"),
]
