from dataclasses import dataclass
from datetime import date
from django.http import HttpResponseForbidden
from datetime import timedelta
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

from habit_tracker.utils import get_todays_completion_percent


from .models import Habit, HabitCompletion, HabitCompletionStatus
from .forms import HabitCompletionForm


class HabitListView(ListView):
    model = Habit
    template_name = "habit_tracker/habit_list.html"
    context_object_name = "habits"
    ordering = ["name"]


class HabitCreateView(CreateView):
    model = Habit
    fields = ["name", "description"]
    template_name = "habit_tracker/habit_create.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class HabitEditView(UpdateView):
    model = Habit
    fields = ["name", "description"]
    template_name = "habit_tracker/habit_edit.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class HabitDeleteView(DeleteView):
    model = Habit
    template_name = "habit_tracker/habit_delete.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class DayView(FormView):
    template_name = "habit_tracker/day.html"
    form_class = HabitCompletionForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["view_date"] = self.view_date
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.view_date = date(kwargs["year"], kwargs["month"], kwargs["day"])

        if self.view_date > date.today():
            return HttpResponseForbidden("Access to future dates is not allowed.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: For each habit, pull how many consecutive days it has been completed
        context["view_date"] = self.view_date
        context["completion_percent"] = round(
            get_todays_completion_percent(self.view_date) * 100
        )
        return context

    def form_valid(self, form):
        completed_habits = form.cleaned_data["habits"]

        for habit in Habit.objects.all():
            status = HabitCompletionStatus.INCOMPLETE

            if habit in completed_habits:
                status = HabitCompletionStatus.COMPLETE

            HabitCompletion.objects.update_or_create(
                habit=habit, date=self.view_date, defaults={"status": status}
            )

        return super().form_valid(form)


@dataclass
class HeatmapData:
    date: date
    completion_percent_float: float
    completion_percent_human_readable: int
    opacity: float


def _find_completion_percent(completions) -> float:
    if not completions:
        return 0.0

    completed_habits = len(
        [c for c in completions if c.status == HabitCompletionStatus.COMPLETE]
    )
    total_habits = len(completions)
    return completed_habits / total_habits


def _find_opacity(completion_percent: float) -> float:
    if completion_percent == 0:
        return 0.0

    # Add a min. opacity so that the heatmap is not completely transparent for days with very few completions
    return max(completion_percent * completion_percent, 0.1)


def heatmap_view(request):
    today = date.today()
    date_to_process = today - timedelta(days=365)
    # Find the Sunday before the day 365 days ago
    while date_to_process.weekday() != 6:
        date_to_process -= timedelta(days=1)
    data = []

    while date_to_process <= today:
        completions = HabitCompletion.objects.filter(date=date_to_process)
        completion_percent = _find_completion_percent(completions)
        day_heatmap_data = HeatmapData(
            date=date_to_process,
            completion_percent_float=completion_percent,
            completion_percent_human_readable=round(completion_percent * 100),
            opacity=_find_opacity(completion_percent),
        )
        data.append(day_heatmap_data)
        date_to_process += timedelta(days=1)

    weeks = []
    for i in range(0, len(data), 7):
        week = data[i : i + 7]
        weeks.append(week)

    return render(request, "habit_tracker/heatmap.html", {"weeks": weeks})


def redirect_today(request):
    today = date.today()
    return redirect(
        "habit_tracker:day_view", year=today.year, month=today.month, day=today.day
    )
