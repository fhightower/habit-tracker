from dataclasses import dataclass
from datetime import date
from django.http import HttpResponseForbidden
from datetime import timedelta
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from habit_tracker.utils import get_habits_for_date
from .models import Habit, HabitCompletion, HabitCompletionStatus
from .forms import HabitCompletionForm


class HabitListView(ListView):
    model = Habit
    template_name = "habit_tracker/habit_list.html"
    context_object_name = "habits"
    ordering = ["name"]


class HabitCreateView(CreateView):
    model = Habit
    fields = ["name", "description", "start_date", "end_date"]
    template_name = "habit_tracker/habit_create.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class HabitEditView(UpdateView):
    model = Habit
    fields = ["name", "description", "start_date", "end_date"]
    template_name = "habit_tracker/habit_edit.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class HabitDeleteView(DeleteView):
    model = Habit
    template_name = "habit_tracker/habit_delete.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


def day_view(request, year, month, day):
    view_date = date(year, month, day)

    if request.method == "POST":
        form = HabitCompletionForm(request.POST, view_date=view_date)
        if form.is_valid():
            for habit in get_habits_for_date(view_date):
                field_name = f"habit_{habit.id}"
                status = form.cleaned_data.get(field_name)
                if status:
                    HabitCompletion.objects.update_or_create(
                        habit=habit,
                        date=view_date,
                        defaults={"status": status},
                    )
            return redirect("habit_tracker:day_view", year=year, month=month, day=day)
    else:
        if view_date > date.today():
            return HttpResponseForbidden("Access to future dates is not allowed.")

        initial_data = {}
        completions = HabitCompletion.objects.filter(date=view_date)
        for completion in completions:
            initial_data[f"habit_{completion.habit.id}"] = completion.status

        form = HabitCompletionForm(initial=initial_data, view_date=view_date)
        context = {
            "form": form,
            "view_date": view_date,
            "completion_percent": round(_find_completion_percent(completions) * 100),
        }

    return render(request, "habit_tracker/day.html", context)


@dataclass
class HeatmapData:
    date: date
    completion_percent_float: float
    completion_percent_human_readable: int
    opacity: float


def _find_completion_percent(completions) -> float:
    if not completions:
        return 0.0

    total_completable_habits = 0
    total_completed_habits = 0

    for completion in completions:
        if completion.status != HabitCompletionStatus.NA:
            total_completable_habits += 1
            if completion.status == HabitCompletionStatus.COMPLETE:
                total_completed_habits += 1

    if total_completable_habits == 0:
        return 0.0

    return total_completed_habits / total_completable_habits


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
    week_stats = []

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
        week_stats.append(
            {
                "avg": round(
                    sum(day.completion_percent_float for day in week) / 7 * 100
                ),
            }
            )

    return render(request, "habit_tracker/heatmap.html", {"week_data": zip(weeks, week_stats)})


def redirect_today(request):
    today = date.today()
    return redirect(
        "habit_tracker:day_view", year=today.year, month=today.month, day=today.day
    )
