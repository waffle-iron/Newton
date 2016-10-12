# scripts/update_account_info.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"
reader_csv="brain/management/commands/usernames_passwords.csv"

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import datetime
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, CurrentClass, Teacher, AccountInfo

import csv
accountReader = csv.reader(open(reader_csv), delimiter=',', quotechar='"')

class Command(BaseCommand):
    help = 'Updates the students usernames and passwords by importing a CSV'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        for row in accountReader:
            if row[0] != 'first':  # Ignore the header row, import everything else
                try:
                    default_data = {}
                    student = StudentRoster.objects.get(first_name=row[0], last_name=row[1])
                    if row[2] != '':
                        default_data['ixluser'] =row[2]
                    if row[3] != '':
                        default_data['ixlpass'] =row[3]
                    if row[4] != '':
                        default_data['kidsazteacher'] =row[4]
                    if row[5] != '':
                        default_data['kidsazuser'] =row[5]
                    if row[6] != '':
                        default_data['kidsazpass'] =row[6]
                    if row[7] != '':
                        default_data['myonuser'] =row[7]
                    if row[8] != '':
                        default_data['myonpass'] =row[8]


                    obj, created = AccountInfo.objects.update_or_create(
                    student=student,
                    defaults=default_data
                    )
                except:
                    pass
