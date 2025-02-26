from django.db import models


class WeeklyQuote(models.Model):
    quote = models.TextField(unique=True)
    last_used = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.quote}"
