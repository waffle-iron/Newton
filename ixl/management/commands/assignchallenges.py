# scripts/import_students.py

# Full path and name to your csv file
# csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/brain/scripts/grade2students2016.csv"

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
from ixl.models import ChallengeAssignment, Challenge

assigned_teachers = ['Trost', 'Mackinnon', "Cyphers", "DaSilva",]
challenge_title = "Fall CBA Challenge"

class Command(BaseCommand):
    help = 'Assigns a challenge to everyone in the classes listed.'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass


    def handle(self, *args, **options):
        for teacher in assigned_teachers:
            try: #Get the class
                current_class = CurrentClass.objects.get(teacher__last_name=teacher)
            except:
                print('Teacher {} could not be found.'.format(teacher))
            print("Getting student list")
            student_list = StudentRoster.objects.filter(current_class=current_class)
            print("Got student list. Getting Challenge.")
            challenge = Challenge.objects.get(title=challenge_title)
            print("Got challenge. Running through list. ")
            for student in student_list:
                print("Assigning to {}".format(student))
                obj, created = ChallengeAssignment.objects.get_or_create(
                    student_id=student, challenge=challenge,
                )
            # Get the student list of that class
            # Iterate through the class list
            # Create the relationship between each kid in the class and the designated challenge
