from datetime import date
from django import forms
from .models import Habit
from .models import HabitCompletionStatus


class HabitCompletionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for habit in Habit.objects.filter().order_by("name"):
            self.fields[f"habit_{habit.id}"] = forms.ChoiceField(
                choices=HabitCompletionStatus.choices,
                widget=forms.Select,
                label=habit.name,
                required=False,
            )

