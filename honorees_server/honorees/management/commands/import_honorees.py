from django.core.management import BaseCommand, CommandError
from honorees.models import *
import csv
import datetime
import sys

def extract(d, keys):
    return dict((k, d[k]) for k in keys if k in d)

class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Imports a CSV file.'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify a CSV file.')
        
        reader = csv.DictReader(open(args[0], 'rU'))
        for row in reader:
            registrant_data = {
                'original_id': row['registrantid'],
                'name': row['registrantname']
            }
            
            registrant, created = Registrant.objects.get_or_create(**registrant_data)
            
            honoree_data = {
                'name': row['separate_honoree'],
                'category': row['category_separate_honoree']
            }
            
            honoree, created = Honoree.objects.get_or_create(**honoree_data)
            
            contribution_data = {
                'year': int(row['year']),
                'received': datetime.datetime.strptime(row['received'], '%m/%d/%y').date(),
                'type': row['type'],
                'registrant': registrant,
                'lobbyist_name': row['lobbyistname'],
                'contribution_type': row['contributiontype'],
                'original_honoree_description': row['honoree_LD203form'],
                'sanitized_honoree_description': row['honoree_cleanedup'],
                'payee': row['payee'],
                'amount': row['amount'],
                'contribution_date': datetime.datetime.strptime(row['received'], '%m/%d/%y').date(),
                'comments': row['comments'],
            }
            
            # only attempt to reuse contribution record if there's more than one honoree
            if ',' in contribution_data['sanitized_honoree_description']:
                contribution, created = Contribution.objects.get_or_create(**contribution_data)
            else:
                contribution = Contribution(**contribution_data)
                contribution.save()
            
            contribution_honoree_data = {
                'contribution': contribution,
                'honoree': honoree,
                'amount': row['divided_amount'],
            }
            
            contribution_honoree = ContributionHonoree(**contribution_honoree_data)
            contribution_honoree.save()