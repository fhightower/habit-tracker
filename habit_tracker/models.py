from datetime import date, timedelta

from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    @property
    def streak(self) -> int:
        today = date.today()
        yesterday = today - timedelta(days=1)

        last_miss = (
            self.completions.filter(status="INCOMPLETE", date__lt=today)
            .order_by("date")
            .last()
        )
        last_completion = (
            self.completions.filter(status="COMPLETE").order_by("date").last()
        )

        # TODO: clean up this function...

        if not last_miss:
            na_completions = self.completions.filter(
                date__range=(self.start_date, today), status=HabitCompletionStatus.NA
            ).count()
            # We +1 b/c you may have gotten it on the start date
            streak = (today - self.start_date).days + 1 - na_completions
            today_completion = self.completions.filter(date=today, habit=self).first()
            if (
                today_completion
                and today_completion.status == HabitCompletionStatus.INCOMPLETE
            ):
                streak -= 1
            return streak

        last_miss_date = last_miss.date
        last_completion_date = last_completion.date if last_completion else date.min

        if last_completion_date > last_miss_date:
            na_completions = self.completions.filter(
                date__range=(last_miss_date, today), status=HabitCompletionStatus.NA
            ).count()
            streak = (today - last_miss_date).days
            today_completion = self.completions.filter(date=today, habit=self).first()
            if (
                today_completion
                and today_completion.status == HabitCompletionStatus.INCOMPLETE
            ):
                streak -= 1
            return streak - na_completions
        else:
            na_completions = self.completions.filter(
                date__range=(last_completion_date, today),
                status=HabitCompletionStatus.NA,
            ).count()
            streak = (yesterday - last_completion_date).days
            return -(streak + na_completions)

    class Meta:
        unique_together = ("name", "start_date", "end_date")

    def __str__(self) -> str:
        return self.name


class HabitCompletionStatus(models.TextChoices):
    INCOMPLETE = "INCOMPLETE", "Incomplete"
    COMPLETE = "COMPLETE", "Complete"
    NA = "N/A", "N/A"


class HabitCompletion(models.Model):
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="completions"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=HabitCompletionStatus.choices,
        default=HabitCompletionStatus.INCOMPLETE,
    )

    class Meta:
        unique_together = ("habit", "date")

    def __str__(self):
        status_icon = "✘"
        if self.status == HabitCompletionStatus.COMPLETE:
            status_icon = "✔"
        if self.status == HabitCompletionStatus.NA:
            status_icon = "-"

        return f"{self.habit.name} on {self.date}: {status_icon}"
