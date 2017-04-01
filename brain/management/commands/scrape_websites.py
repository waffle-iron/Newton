# scripts/import_students.py


student_csv="brain/management/commands/grade2students2016.csv"

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

from django.core.management.base import BaseCommand, CommandError
from brain.models import StudentRoster, CurrentClass, Teacher
from brain.scripts.webscrape import run_all_teachers
from ixl.models import IXLSkill, IXLSkillScores, IXLStats

import csv


class Command(BaseCommand):
    help = 'Scrapes IXL and myON for our data'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass




    def handle(self, *args, **options):

        run_all_teachers() # Scrapes all the information we need

