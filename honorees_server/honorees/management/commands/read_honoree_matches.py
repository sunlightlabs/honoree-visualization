from django.core.management import BaseCommand, CommandError
from honorees.models import *
import csv

class Command(BaseCommand):
    args = '<csv>'
    help = 'Read in hand-edited legislator and party info.'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify a CSV file.')
        
        infile = args[0]
        
        file = open(infile, 'rbU')
        csvfile = csv.DictReader(file)
        
        for honoree in csvfile:
            try:
                db_honoree = Honoree.objects.get(name=honoree['name'])
            except:
                print '%s failed; aborting.' % honoree['name']
                return
            db_honoree.party = honoree['party']
            db_honoree.state = honoree['state']
            db_honoree.save()
        
        file.close()