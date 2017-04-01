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
from ixl.models import ChallengeAssignment, Challenge, ChallengeExercise, IXLSkillScores
from libs.functions import nwea_recommended_skills_list as nwea_skills


assigned_teachers = ['Cyphers', 'Trost', 'Mackinnon']
teachers_addition = 'D-A.4'

class Command(BaseCommand):
    help = 'Assigns a custom challenge to everyone in the classes listed.'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass


    def handle(self, *args, **options):
        for teacher in assigned_teachers:
            try: #Get the class
                current_class = CurrentClass.objects.get(teacher__last_name=teacher)
            except:
                print('Teacher {} could not be found.'.format(teacher))
                break
            print("Getting student list")
            student_list = StudentRoster.objects.filter(current_class=current_class)
            print("Got student list. Creating Challenges.")
            for student in student_list: #Go through one student at a time
                domain_list = []
                # Create the new Challenge
                #print("Setting the date")
                date = datetime.date.today()
                #print("Set the date. Formatting date with strf time")
                date = date.strftime('%-m/%-d')
                #print("Formatted the date. Setting the title with format")

                title = "{} {}'s {} Challenge".format(student.first_name, student.last_name[0],date)
                #print("Creating current challenge.")
                todays_date = datetime.date.today()
                current_challenge = Challenge.objects.create(title=title, date=todays_date)

                skill_list = nwea_skills(student,"recommended_skill_list")

                exercise_count = 0
                if teachers_addition != "None":
                    try:
                        skill_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=teachers_addition)
                        if skill_score.score < 96:
                            exercise_count = 1
                            challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge, exercise_id=teachers_addition,
                                                                                  required_score=100,)
                    except:
                        exercise_count = 1
                        challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                              exercise_id=teachers_addition,
                                                                              required_score = 100)

                for skill in skill_list:
                    if skill[3] in domain_list or exercise_count >= 5:
                        pass
                    else:

                        domain_list.append(skill[3]) # Add this domain to the list
                        # Create a Challenge Exercise object with the challenge and skill
                        try:
                            challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                                  exercise_id=skill[0])
                            exercise_count += 1
                        except:
                            continue
                if exercise_count <5:
                    for skill in skill_list:
                        matching_skill = ChallengeExercise.objects.filter(challenge=current_challenge, exercise_id=skill[0])
                        if not matching_skill.count():
                            try:
                                challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                                      exercise_id=skill[0])
                                exercise_count += 1
                            except:
                                continue
                        if exercise_count>=5:
                            break

                print("Assigning {} to {}, length: {}".format(title,student, exercise_count))

                obj, created = ChallengeAssignment.objects.get_or_create(
                    student_id=student, challenge=current_challenge,
                )
            # Get the student list of that class
            # Iterate through the class list
            # Create the relationship between each kid in the class and the designated challenge
