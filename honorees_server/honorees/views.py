from django.http import HttpResponse
import json
from honorees.models import *
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

def all_honorees(request):
    category_mappings = {
        'E': 'executive',
        'Rep/Sen': 'congress',
        'D': 'delegation',
        '': 'other',
        'O': 'other',
        'L': 'legislative',
    }
    out = [
        {
            'id': honoree.id,
            'total_contributions': int(round(honoree.total_contributions)),
            'contribution_count': honoree.contribution_count,
            'name': honoree.name,
            'party': honoree.party,
            'state': honoree.state,
            'category': category_mappings.get(str(honoree.category), 'executive')
        }
        for honoree in Honoree.objects.all().annotate(total_contributions=Sum('contributionhonoree__amount'), contribution_count=Count('contributionhonoree')).order_by('-total_contributions')
    ]
    return HttpResponse(json.dumps(out), content_type='application/json')

def all_registrants(request):
    out = [
        {
            'id': registrant.id,
            'total_contributions': int(round(registrant.total_contributions)),
            'contribution_count': registrant.contribution_count,
            'name': registrant.standardized_name
        }
        for registrant in Registrant.objects.all().annotate(total_contributions=Sum('contribution__amount'), contribution_count=Count('contribution')).order_by('-total_contributions')
    ]
    return HttpResponse(json.dumps(out), content_type='application/json')

def entity(request, type, id):
    model = Registrant if type == 'registrant' else Honoree
    obj = get_object_or_404(model, id=id)
    out = [
        {
            'registrant': contribution.registrant.standardized_name,
            'honorees': ", ".join([honoree.name for honoree in contribution.honorees.all()]),
            'payee': contribution.payee,
            'amount': int(round(contribution.amount)) if type == 'registrant' else int(round(contribution.contributionhonoree_set.filter(honoree=obj)[0].amount)),
            'date': contribution.contribution_date.strftime("%m/%d/%Y")
        }
        for contribution in obj.contribution_set.all().order_by('-amount').select_related()
    ]
    return HttpResponse(json.dumps(out), content_type='application/json')