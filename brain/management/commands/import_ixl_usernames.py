# scripts/update_account_info.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"
reader_csv="brain/management/commands/ixlpasswords.csv"

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
            try:
                student = StudentRoster.objects.get(last_name=row[0], first_name=row[1])
                ixluser = row[2]
                ixlpass = row[3]
                updated_values = {'ixluser': ixluser, 'ixlpass': ixlpass}
                obj, created = AccountInfo.objects.update_or_create(
                    student=student, defaults=updated_values)
            except:
                pass
