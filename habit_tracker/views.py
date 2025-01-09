from datetime import date
from django.views.generic import (
    CreateView,
    DayArchiveView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)
from django.urls import reverse_lazy


from .models import Habit, HabitCompletion
from .forms import HabitCompletionForm


# todo: create edit option for habits
# todo: create delete option for habits


class HabitListView(ListView):
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


class HabitDeleteView(DeleteView):
    model = Habit
    template_name = "habit_tracker/habit_delete.html"
    success_url = reverse_lazy("habit_tracker:habit_list")


class HabitCompletionDayArchiveView(DayArchiveView):
    queryset = HabitCompletion.objects.all()
    date_field = "date"
    allow_future = True


class TodayView(FormView):
    template_name = "habit_tracker/today.html"
    form_class = HabitCompletionForm
    success_url = reverse_lazy("habit_tracker:today")

    def form_valid(self, form):
        completed_habits = form.cleaned_data["habits"]
        today = date.today()

        todays_habit_completions = HabitCompletion.objects.filter(date=today)

        for habit_completion in todays_habit_completions:
            if habit_completion.habit not in completed_habits:
                habit_completion.delete()

        for habit in completed_habits:
            HabitCompletion.objects.update_or_create(habit=habit, date=today)

        return super().form_valid(form)
