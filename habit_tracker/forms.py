from datetime import date
from django import forms
from habit_tracker.utils import get_habits_for_date
from .models import HabitCompletionStatus

# Create a class that extends forms.ChoiceField and allows for a notes field
class CustomChoiceField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.note = kwargs.pop("note", None)
        super().__init__(*args, **kwargs)

    def get_bound_field(self, form, field_name):
        bound_field = super().get_bound_field(form, field_name)
        bound_field.note = self.note
        return bound_field


class HabitCompletionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        view_date = kwargs.pop("view_date")
        is_today = kwargs.pop("is_today")
        super().__init__(*args, **kwargs)

        for habit in get_habits_for_date(view_date):
            label = habit.name
            if is_today:
                label += f" (streak: {habit.streak})"
            self.fields[f"habit_{habit.id}"] = CustomChoiceField(
                choices=HabitCompletionStatus.choices,
                widget=forms.Select,
                label=label,
                required=False,
                note=self.initial.get(f"note_habit_{habit.id}") or "",
            )
