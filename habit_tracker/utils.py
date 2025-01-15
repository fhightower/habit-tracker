from datetime import date

from habit_tracker.models import Habit, HabitCompletion

def get_todays_completion_percent(date: date) -> float:
    return HabitCompletion.objects.filter(date=date, status="COMPLETE").count() / Habit.objects.count()

