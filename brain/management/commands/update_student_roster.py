# scripts/import_students.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"
student_csv="brain/management/commands/grade2students2016.csv"
teacher_csv="brain/management/commands/teacherlist.csv"
class_csv="brain/management/commands/classlist.csv"

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import datetime
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, CurrentClass, Teacher

import csv
studentReader = csv.reader(open(student_csv), delimiter=',', quotechar='"')
teacherReader = csv.reader(open(teacher_csv), delimiter=',', quotechar='"')
classReader = csv.reader(open(class_csv), delimiter=',', quotechar='"')




class Command(BaseCommand):
    help = 'Updates the teachers and student Roster by importing a CSV'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass




    def handle(self, *args, **options):
        for row in teacherReader:
            if row[0] != 'Last Name':  # Ignore the header row, import everything else
                title = row[0]
                first_name = row[1]
                last_name = row[2]

                obj, created = Teacher.objects.get_or_create(
                    last_name=last_name,
                    first_name=first_name,
                    title=title,
                )

        for row in classReader:
            if row[0] != 'Last Name':  # Ignore the header row, import everything else
                year = row[0]
                grade = row[1]
                teacher = Teacher.objects.all().get(last_name=row[2])
                obj, created = CurrentClass.objects.get_or_create(
                    year=year,
                    grade=grade,
                    teacher=teacher,
                )

        for row in studentReader:
            if row[0] != 'Last Name':  # Ignore the header row, import everything else
                last_name = row[0]
                first_name = row[1]
                date_of_birth = datetime.datetime.strptime(row[2], "%m/%d/%y").strftime('%Y-%m-%d')
                gender = row[3]
                current_class = CurrentClass.objects.all().get(teacher__last_name=row[4])
                obj, created = StudentRoster.objects.get_or_create(
                    last_name=last_name,
                    first_name=first_name,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    current_class=current_class,
                )