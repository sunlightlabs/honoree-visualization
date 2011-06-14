from django.core.management import BaseCommand, CommandError
from honorees.models import *
import csv

def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)

class Command(BaseCommand):
    args = '<csv>'
    help = 'Output auto-matched legislator and party info.'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify a CSV file.')
        
        out = args[0]
        
        file = open(out, 'w')
        csvfile = csv.DictWriter(file, ['name', 'party', 'state'])
        csvfile.writeheader()
        
        for honoree in Honoree.objects.filter(category='Rep/Sen').order_by('state'):
            csvfile.writerow({
                'name': honoree.name,
                'party': honoree.party if honoree.party != '0' else '',
                'state': honoree.state
            })
        
        file.close()