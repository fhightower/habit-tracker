from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add date fields for start and end dates
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("name", "start_date", "end_date")

    def __str__(self):
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
