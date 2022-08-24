from time import time
from django.db import models
from django.utils.timezone import localtime


def duration_visits(visit, passcard, minutes=60):
    this_passcard_visits = []
    visits = Visit.objects.filter(passcard=passcard)

    for visit in visits:
        entered_at = localtime(visit.entered_at)
        if visit.leaved_at:
            leaved_at = localtime(visit.leaved_at)
        else:
            leaved_at = localtime()
        delta = get_duration(leaved_at, entered_at)
        delta_minutes = delta // 60
        duration = format_duration(delta)
        is_flag = delta_minutes >= minutes
        visit_stange = {
            'entered_at': f'{entered_at}',
            'duration': f'{duration}',
            'is_strange': is_flag
            }
        this_passcard_visits.append(visit_stange)
    return this_passcard_visits


def visits_not_leaved(visit):
    now_time = localtime()
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in visits:
        who_entered = visit.passcard
        entered_at = localtime(visit.entered_at)
        delta = get_duration(now_time, entered_at)
        duration = format_duration(delta)
        dict_visit = {
            'who_entered': f'{who_entered}',
            'entered_at': f'{entered_at}',
            'duration': f'{duration}',
        }
        non_closed_visits.append(dict_visit)
    return non_closed_visits


def get_duration(now_at, entered_at):
    return (now_at - entered_at).total_seconds()


def format_duration(duration):
    days = duration // 86400
    hours = (duration - (days * 86400)) // 3600
    minutes = (duration - (days * 86400) - (hours * 3600)) // 60
    timedelta_format = f'{int(days)} дней {int(hours)} часов \
        {int(minutes)} минут'
    return timedelta_format


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
