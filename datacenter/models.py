from time import time
from django.db import models
from django.utils.timezone import localtime
MAX_MINUTES_DURATION = 60


def get_visits_by_passcard(passcard, max_minutes_duraition: int = MAX_MINUTES_DURATION):
    this_passcard_visits = []
    visits = Visit.objects.filter(passcard=passcard)

    for visit in visits:
        delta = get_duration(visit)
        entered_at = localtime(visit.entered_at)
        is_strange = is_visit_long(delta, max_minutes_duraition)
        duration = format_duration(delta)
        visit_stange = {
            'entered_at': f'{entered_at}',
            'duration': f'{duration}',
            'is_strange': is_strange
            }
        this_passcard_visits.append(visit_stange)
    return this_passcard_visits


def get_non_closed_visits():
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in visits:
        entered_at = localtime(visit.entered_at)
        delta = get_duration(visit)
        duration = format_duration(delta)
        dict_visit = {
            'who_entered': f'{visit.passcard}',
            'entered_at': f'{entered_at}',
            'duration': f'{duration}',
        }
        non_closed_visits.append(dict_visit)
    return non_closed_visits


def get_duration(visit) -> int:
    entered_at = localtime(visit.entered_at)
    if visit.leaved_at:
        leaved_at = localtime(visit.leaved_at)
    else:
        leaved_at = localtime()
    return (leaved_at - entered_at).total_seconds()


def format_duration(duration):
    days = duration // 86400
    hours = (duration - (days * 86400)) // 3600
    minutes = (duration - (days * 86400) - (hours * 3600)) // 60
    timedelta_format = f'{int(days)} дней {int(hours)} часов \
        {int(minutes)} минут'
    return timedelta_format

def is_visit_long(delta, max_minutes_duraition):
    delta_minutes = delta // 60
    is_strange = delta_minutes >= max_minutes_duraition
    return is_strange



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
