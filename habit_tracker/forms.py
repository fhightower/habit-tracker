from datetime import date, timedelta
from django import forms
from .models import Habit


class HabitCompletionForm(forms.Form):
    habits = forms.ModelMultipleChoiceField(
        queryset=Habit.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        label="",
    )

    def __init__(self, *args, **kwargs):
        view_date = kwargs.pop('view_date', date.today())
        super().__init__(*args, **kwargs)

        completed_habits = Habit.objects.filter(
            completions__date=view_date,
            completions__status="COMPLETE",
        )

        self.fields["habits"].initial = completed_habits
