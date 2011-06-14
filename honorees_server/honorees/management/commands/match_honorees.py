from django.core.management import BaseCommand, CommandError
from honorees.models import *
import json
import urllib, urllib2
import settings
import re

def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)

class Command(BaseCommand):
    def handle(self, *args, **options):
        titles = re.compile(r'\w{3}\. ')
        
        for honoree in Honoree.objects.filter(category='Rep/Sen'):
            name = titles.sub('', honoree.name)
            
            data = json.loads(
                urllib2.urlopen("http://transparencydata.com/api/1.0/entities.json?" + urllib.urlencode({
                    "apikey": settings.API_KEY,
                    "search": name
                })).read()
            )
            
            pols = [record for record in data if record['type'] == 'politician' and record['seat'] in ('federal:senate', 'federal:house')]
            
            if len(pols) == 1 or (len(pols) == 2 and pols[0]['seat'] != pols[1]['seat']):
                honoree.state = pols[0]['state']
                honoree.party = pols[0]['party']
                honoree.save()
                
                print 'Updated %s' % name