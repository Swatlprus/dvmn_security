from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import visits_not_leaved
from django.shortcuts import render



def storage_information_view(request):

    non_closed_visits = visits_not_leaved(request)
    
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
