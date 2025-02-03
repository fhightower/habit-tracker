from datetime import date

from django.db.models import Q

from habit_tracker.models import Habit, HabitCompletion

def get_todays_completion_percent(date: date) -> float:
    return HabitCompletion.objects.filter(date=date, status="COMPLETE").count() / get_habits_for_date(date).count()


def get_habits_for_date(date: date) -> list[Habit]:
    end_date_query = Q(end_date__gte=date) | Q(end_date__isnull=True)
    return Habit.objects.filter(start_date__lte=date).filter(end_date_query).order_by("name")

