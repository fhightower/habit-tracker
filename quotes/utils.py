from datetime import timedelta

from django.utils import timezone

from .models import WeeklyQuote


def get_most_recent_weekly_quote() -> WeeklyQuote:
    return WeeklyQuote.objects.order_by("-last_used").first()


def get_random_weekly_quote() -> WeeklyQuote:
    return WeeklyQuote.objects.order_by("?").first()


def choose_quote(quote: WeeklyQuote) -> WeeklyQuote:
    # Set the last_used date to the Sunday before the current date unless today is Sunday
    now = timezone.now()
    weekday = now.weekday()
    now_date = now.date()

    last_sunday = now_date - timedelta(days=weekday + 1)
    quote.last_used = last_sunday
    if weekday == 6:
        quote.last_used = now_date
    quote.save()
    return quote


def get_quote_for_week() -> WeeklyQuote:
    quote = get_most_recent_weekly_quote()

    if (
        not quote
        or not quote.last_used
        or quote.last_used < timezone.now().date() - timedelta(days=7)
    ):
        quote = choose_quote(get_random_weekly_quote())

    return quote
