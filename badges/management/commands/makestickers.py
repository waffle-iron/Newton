
sticker_csv="badges/management/commands/stickerlist.csv"

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
from datetime import date
import sys,os
from os import listdir
import re

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
import random
from django.core.management.base import BaseCommand, CommandError
from brain.models import StudentRoster, CurrentClass, Teacher
from badges.models import Sticker
from brain.scripts.webscrape import run_all_teachers
from ixl.models import IXLSkill, IXLSkillScores, IXLStats

import csv

STICKERS = ['alvin.png', 'anger.png', 'anna.png', 'baymax.png', 'bb8.png', 'beastboy.png', 'benny.png',
 'blastoise.png', 'bowser.png', 'buzzlightyear.png', 'captainman.png', 'charizard.png',
 'clifford.png', 'creeper.png', 'curiousgeorge.png', 'cyborg.png', 'darthvader.png', 'donatello.png', 'dory.png',
 'elsa.png', 'emmett.png', 'everafterhigh1.png', 'everafterhigh2.png', 'everafterhigh3.png', 'everafterhigh4.png',
 'finn.png', 'henrydanger.png', 'jake.png', 'joy.png', 'legobatman.png', 'legoblackpanther.png', 'legoblackwidow.png',
 'legocaptainamerica.png', 'legospiderman.png', 'legosuperman.png', 'legowolverine.png', 'legowonderwoman.png',
 'leonardo.png', 'lightingmcqueen.png', 'littleeinsteinsjune.png', 'littleeinsteinsleo.png',
 'littleeinsteinsquincy.png', 'luigi.png', 'mario.png', 'mariostar.png', 'mater.png', 'mickey.png', 'mike.png',
 'mikey.png', 'minion1.png', 'minion2.png', 'minion3.png', 'minnie.png', 'monsterhigh1.png', 'monsterhigh2.png',
 'monsterhigh3.png', 'monsterhighlogo.png', 'nemo.png', 'olaf.png', 'optimusprime.png', 'patrick.png', 'peach.png',
 'pikachu.png', 'pokeball.png', 'r2d2.png', 'raphael.png', 'robin.png', 'scoobydoo.png', 'simon.png', 'spongebob.png',
 'squidward.png', 'starlord.png', 'steve.png', 'stormtrooper.png', 'sully.png', 'theodore.png', 'toad.png',
 'wildstyle.png', 'woody.png', 'yoshi.png']

class Command(BaseCommand):
    help = 'Makes sticker objects for achievements'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        # Get the CSV into an object
        random.shuffle(STICKERS)
        dataReader = csv.reader(open(sticker_csv), delimiter=',', quotechar='"')
        # For row in the CSV, get name, slug, description
        for row in dataReader:
            if row[0] != 'name':  # Ignore the header row, import everything else
                name = row[0]
                slug = row[1]
                description = row[2]
                image = "static/images/stickers/{}".format(STICKERS.pop())
                category = row[3]
                order = row[4]
                obj, created = Sticker.objects.update_or_create(slug=slug,
                                                                defaults={'name':name, 'description':description,
                                                                          'image':image, 'category':category,
                                                                          'order':order,},
                )




