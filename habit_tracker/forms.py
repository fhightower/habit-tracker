from datetime import date
from django import forms
from habit_tracker.utils import get_habits_for_date
from .models import HabitCompletionStatus


class HabitCompletionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        view_date = kwargs.pop("view_date")
        is_today = kwargs.pop("is_today")
        super().__init__(*args, **kwargs)

        for habit in get_habits_for_date(view_date):
            label = habit.name
            if is_today:
                label += f" (streak: {habit.streak})"
            self.fields[f"habit_{habit.id}"] = forms.ChoiceField(
                choices=HabitCompletionStatus.choices,
                widget=forms.Select,
                label=label,
                required=False,
            )
