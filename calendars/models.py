from django.db import models

from common.models import CommonModel


class Calendar(CommonModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="user_calendar"
    )
    title = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="unique_calendar")
        ]


class Schedule(CommonModel):
    calendar = models.ForeignKey(
        "calendars.Calendar",
        on_delete=models.CASCADE,
        related_name="calendar_schedule",
    )
    participant = models.ManyToManyField("users.User", related_name="user_schedule")
    memo = models.OneToOneField(
        "memos.Memo", on_delete=models.CASCADE, related_name="memo_schedule", null=True
    )
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    start_time = models.TimeField(null=True)
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)
    is_repeat = models.BooleanField(default=False)
