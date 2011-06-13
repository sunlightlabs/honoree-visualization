from django.core.management import BaseCommand, CommandError
from honorees.models import *
import os, shutil
from honorees.views import *
import settings
from django.shortcuts import render_to_response

def ensure_directory(dir):
    if not (os.path.exists(dir) and os.path.isdir(dir)):
        os.mkdir(dir)

class Command(BaseCommand):
    args = '<directory>'
    help = 'Collapses files into one directory'
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please specify a directory.')
        
        directory = args[0]
        
        # check that directories exists
        ensure_directory(directory)
        os.chdir(directory)
        
        ensure_directory('honoree')
        ensure_directory('registrant')
        
        # index and JS
        index = open('index.html', 'w')
        index.write(render_to_response('honorees/index.html', {}).content)
        index.close()
        
        js = open('honorees.js', 'w')
        js.write(render_to_response('honorees/honorees.js', {}).content)
        js.close()
        
        # overall listings
        registrants = open('all_registrants.json', 'w')
        registrants.write(all_registrants(None).content)
        registrants.close()
        
        honorees = open('all_honorees.json', 'w')
        honorees.write(all_honorees(None).content)
        honorees.close()
        
        # individual records
        for t in [('registrant', Registrant), ('honoree', Honoree)]:
            for record in t[1].objects.all():
                out_file = open('%s/%s.json' % (t[0], record.id), 'w')
                out_file.write(entity(None, t[0], record.id).content)
                out_file.close()
        
        # media
        if os.path.exists('media'):
            shutil.rmtree('media')
        shutil.copytree(settings.MEDIA_ROOT, 'media')