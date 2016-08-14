# scripts/import_students.py

# Full path and name to your csv file
csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django
import datetime
import sys,os
sys.path.append(your_djangoproject_home)
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
from brain.models import StudentRoster, Teacher, CurrentClass


import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

# Start execution
def run():
    for row in dataReader:
        if row[0] != 'Last Name': # Ignore the header row, import everything else
            student = StudentRoster()
            student.last_name = row[0]
            student.first_name = row[1]
            DOB = datetime.datetime.strptime(row[2], "%m/%d/%y").strftime('%Y-%m-%d')
            student.date_of_birth = DOB
            student.gender = row[3]
            current_class = CurrentClass.objects.all().get(teacher__last_name=row[4])
            student.current_class = current_class
            student.save()
            print(student)
            print(student.current_class)

run()
#YYY-MM-DD