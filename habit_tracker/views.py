from datetime import date
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect


from .models import Habit, HabitCompletion, HabitCompletionStatus
from .forms import HabitCompletionForm


class HabitListView(ListView):
    # TODO: sort by alphabetical order
    model = Habit
    template_name = "habit_tracker/habit_list.html"
    context_object_name = "habits"


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


# TODO: block access to future dates


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
        return super().dispatch(request, *args, **kwargs)

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


def redirect_to_today(request):
    today = date.today()
    return redirect(
        "habit_tracker:day_view", year=today.year, month=today.month, day=today.day
    )
