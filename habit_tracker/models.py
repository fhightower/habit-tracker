from django.db import models


class Habit(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitCompletion(models.Model):
    habit = models.ForeignKey(
        Habit, on_delete=models.CASCADE, related_name="completions"
    )
    date = models.DateField()

    class Meta:
        unique_together = ("habit", "date")

    def __str__(self):
        return f"{self.habit.name} on {self.date}: ✔"
