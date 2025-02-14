from datetime import date

from django.db.models import Q

from habit_tracker.models import Habit, HabitCompletion


def get_date_completion_percent(desired_date: date) -> float:
    return (
        HabitCompletion.objects.filter(date=desired_date, status="COMPLETE").count()
        / get_habits_for_date(desired_date).count()
    )


def get_habits_for_date(desired_date: date) -> list[Habit]:
    end_date_query = Q(end_date__gte=desired_date) | Q(end_date__isnull=True)
    return (
        Habit.objects.filter(start_date__lte=desired_date)
        .filter(end_date_query)
        .order_by("name")
    )
