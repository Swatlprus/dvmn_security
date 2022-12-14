from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_visits_by_passcard
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):

    passcard = get_object_or_404(Passcard, passcode=passcode)
        
    this_passcard_visits = get_visits_by_passcard(passcard)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
