import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Reminder(models.Model):
    class AlertCount(models.IntegerChoices):
        ZERO = 0
        FIRST = 1
        SECOND = 2

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        related_name="reminder_user",
    )
    title = models.CharField(_("title"), max_length=32)
    message = models.TextField(
        null=True, blank=True, verbose_name=_("message")
    )

    image = models.ForeignKey(
        "storage.MediaModel",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="upload_image",
    )

    reminder_time = models.DateTimeField(
        verbose_name=_("reminder time"),
    )

    threshold = models.DateTimeField(
        verbose_name=_("remind before"),
    )

    alert_count = models.IntegerField(
        choices=AlertCount.choices,
        default=AlertCount.ZERO,
        verbose_name=_("alert count"),
    )

    REPEAT_CHOICES = (
        ("DONT_REPEAT", _("dont repeat")),
        ("DAILY", _("daily")),
        ("MONTHLY", _("monthly")),
    )

    repeat_interval = models.CharField(
        verbose_name=_("repeat interval"),
        max_length=20,
        choices=REPEAT_CHOICES,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is active"),
    )

    created_at = models.DateField(
        auto_now_add=True, verbose_name=_("created at")
    )

    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    def clean(self):
        super(Reminder, self).clean()
        if self.threshold >= self.reminder_time:
            raise ValidationError(
                _(
                    "threshold should be less than reminder time, please enter correct threshold"
                ),
            )
        if self.alert_count == 2 and self.is_active == True:
            raise ValidationError(
                _(
                    "alert count amount for activating reminder could not be two"
                )
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Reminder, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"
