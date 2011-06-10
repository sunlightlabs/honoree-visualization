from django.http import HttpResponse
import json
from honorees.models import *
from django.db.models import Count, Sum

def all_honorees(request):
    out = [
        {
            'id': honoree.id,
            'total_contributions': int(round(honoree.total_contributions)),
            'contribution_count': honoree.contribution_count,
            'name': honoree.name
        }
        for honoree in Honoree.objects.all().annotate(total_contributions=Sum('contributionhonoree__amount'), contribution_count=Count('contributionhonoree')).order_by('-total_contributions')
    ]
    return HttpResponse(json.dumps(out), content_type='application/json')