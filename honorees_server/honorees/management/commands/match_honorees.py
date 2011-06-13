from django.core.management import BaseCommand, CommandError
from honorees.models import *
import json
import urllib, urllib2
import settings

def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for honoree in Honoree.objects.filter(category='Rep/Sen'):
            name = honoree.name.replace('Rep.', '').replace('Sen.', '').strip()
            
            data = json.loads(
                urllib2.urlopen("http://transparencydata.com/api/1.0/entities.json?" + urllib.urlencode({
                    "apikey": settings.API_KEY,
                    "search": name
                })).read()
            )
            
            pols = [record for record in data if record['type'] == 'politician']
            
            if len(pols) == 1:
                honoree.state = pols[0]['state']
                honoree.party = pols[0]['party']
                honoree.save()
                
                print 'Updated %s' % name