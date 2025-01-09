from datetime import date
from django import forms
from .models import Habit


class HabitCompletionForm(forms.Form):
    # TODO: start here and sort by habit name
    habits = forms.ModelMultipleChoiceField(
        queryset=Habit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()

        # Get habits that have a completion record for today
        completed_habits = Habit.objects.filter(
            completions__date=today,
        )

        self.fields["habits"].initial = completed_habits
