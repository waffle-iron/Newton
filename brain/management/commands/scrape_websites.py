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


    #     csv_list = listdir('brain/scripts/csvdownloads') # Gets the downloaded file list from the directory
    #     lexile_files = []
    #     score_grid_files = []
    #     ixl_stats_files = []
    #     for x in range(len(csv_list)): # Starts to sort all the data into 1 csv for each data type
    #         current_file = csv_list[x]
    #         # Figure out which file we're working with (lexile, Score-Grid, or ixlstats)
    #         if 'lexile' in current_file:
    #             lexile_files.append(current_file)
    #         elif 'Score-Grid' in current_file:
    #             score_grid_files.append(current_file)
    #         elif 'ixlstats' in current_file:
    #             ixl_stats_files.append(current_file)
    #         else:
    #             print("File {} Not Recognized".format(current_file))
    #
    #     # Read through all lexile files in list and put the information into 1 csv
    #     for file in lexile_files:
    #         dataReader = csv.reader(open('brain/scripts/csvdownloads/'+ file), delimiter=',', quotechar='"')
    #         outputFile = open('brain/scripts/csvuploads/{}.csv'.format('lexile'), 'w', newline='')
    #         outputWriter = csv.writer(outputFile)
    #         for row in dataReader:
    #             if row[0] != 'student_user_id':
    #                 outputWriter.writerow([row[2], row[3], row[12], row[8]])
    #     outputFile.close()
    #
    #
    #     # Read through all Score-Grid files in list and put the information into 1 csv
    #     for file in score_grid_files:
    #         dataReader = csv.reader(open('brain/scripts/csvdownloads/'+ file), delimiter=',', quotechar='"')
    #         outputFile = open('brain/scripts/csvuploads/{}.csv'.format('ixl-score-grid'), 'w', newline='')
    #         outputWriter = csv.writer(outputFile)
    #         for row in dataReader:
    #             if row[0] != 'student_user_id':
    #                 outputWriter.writerow([row[2], row[3], row[12], row[8]])
    #     outputFile.close()
    #
    #     # Read through all Score-Grid files in list and put the information into 1 csv
    #
    #
    # def unpack_lexile(self):
    #     pass
    #
    #
    # def unpack_score_grid(self, file_name): # Takes



#0 student_user_id
#1 student_student_id
#2 student_name_last
#3 student_name_first
#4 student_user_grade_level_id
#5 user_grade_level
#6 earliest_lexile
#7 earliest_lexile_date
#8 latest_lexile
#9 latest_lexile_date
#10 prior_lexile
#11 prior_lexile_date
#12 assessment_count
#13 lexile_progress
