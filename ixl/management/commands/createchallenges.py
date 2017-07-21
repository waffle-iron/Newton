# commands/createchallenges.py

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import datetime
import sys,os
import requests
from variables import second_teachers as assigned_teachers
from variables import mastery_skills, cbaExercises
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, CurrentClass, Teacher
from ixl.models import ChallengeAssignment, Challenge, ChallengeExercise, IXLSkillScores
from libs.functions import nwea_recommended_skills_list as nwea_skills

date = datetime.date.today()
date = date.strftime('%-m/%-d')
todays_date = datetime.date.today()


class Command(BaseCommand):
    help = 'Assigns a custom challenge to all students'

    def add_arguments(self, parser):
        pass

    def make_mastery_challenge(self, student, current_challenge, exercise_count):
        for addition in mastery_skills:
            try:
                skill_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=addition)
                if skill_score.score < 96:
                    exercise_count += 1
                    challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                          exercise_id=addition,
                                                                          required_score=100, )
            except:
                exercise_count += 1
                challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                      exercise_id=addition,
                                                                      required_score=100)
            if exercise_count == 1:
                return exercise_count
        return exercise_count


    def make_cba_challenge(self, student, current_challenge, exercise_count):
        for addition in cbaExercises:
            try:
                skill_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=addition)
                if skill_score.score < 78:
                    exercise_count += 1
                    challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                      exercise_id=addition,
                                                                      required_score=80, )
                else:
                    print("Could not add {}".format(addition))
            except:

                try:
                    challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                      exercise_id=addition,
                                                                      required_score=80)
                    exercise_count += 1
                except:
                    pass

            if exercise_count == 3:
                return exercise_count

        print("Ran out of cba exercises for {}!".format(student))
        return exercise_count


    def make_nwea_challenge(self, student, current_challenge, exercise_count):
        skill_list = nwea_skills(student, "recommended_skill_list")
        domain_list = []
        waiting_list = []
        for skill in skill_list:
            previously_assigned = ChallengeExercise.objects.filter(challenge__challengeassignment__student_id=student, exercise_id=skill[0] )
            pal = len(previously_assigned)
            print("{} Previously Assigned {} times".format(skill[0],pal))
            if pal>3:
                continue
            if skill[3] in domain_list:
                waiting_list.append(skill[0])
            elif exercise_count >=5:
                waiting_list.append(skill[0])
            else:
                domain_list.append(skill[3])  # Add this domain to the list
                # Create a Challenge Exercise object with the challenge and skill
                try:
                    challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                          exercise_id=skill[0])
                    exercise_count += 1
                except:
                    continue
        if exercise_count<5:
            for skill in waiting_list:

                try:
                    challenge_exercise = ChallengeExercise.objects.create(challenge=current_challenge,
                                                                          exercise_id=skill[0])
                    exercise_count += 1
                except:
                    continue
                if exercise_count ==5:
                    return exercise_count


        return exercise_count



    def handle(self, *args, **options):

        for teacher in assigned_teachers:
            try: #Get the class
                current_class = CurrentClass.objects.get(teacher__last_name=teacher)
            except:
                print('Teacher {} could not be found.'.format(teacher))
                break
            student_list = StudentRoster.objects.filter(current_class=current_class)
            print("Got student list. Creating Challenges.")
            for student in student_list: #Go through one student at a time
                title = "{} {}'s {} Challenge".format(student.first_name, student.last_name[0],date)
                current_challenge = Challenge.objects.create(title=title, date=todays_date)
                exercise_count = 0
                exercise_count = self.make_mastery_challenge(student, current_challenge, exercise_count)
                exercise_count = self.make_cba_challenge(student, current_challenge, exercise_count)
                exercise_count = self.make_nwea_challenge(student, current_challenge, exercise_count)


                print("Assigning {} to {}, length: {}".format(title,student, exercise_count))

                obj, created = ChallengeAssignment.objects.get_or_create(
                    student_id=student, challenge=current_challenge,
                )

#TODO: Email teachers previous week's scores
# TODO: Add Bonus Exercises
# IXL Challenge Creation
# Create 5 main challenges
    # 2 for CBA
        # Map the CBAs to IXL Exercises for each of the three.
            # Make it change depending on the date
    # 2 for NWEA
    # 1 for Mastery - based on the current or passed curriculum - 100 Smart Score
# Create 5 Bonus Challenges

from django.core.mail import EmailMessage
def send_an_email():
    email = EmailMessage(
        subject='Hello',
        body='''Body goes here.
             How are you?
             I hope this email works!''',
        from_email='newton@newtonthinks.com',
        to=['ins-dauaprqb@isnotspam.com'],
        reply_to=['alextrostbtwa@gmail.com.com'],
        headers={'Content-Type': 'text/plain'},
    )
    email.send()



def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox791822b6aeca4aee8007134fecd331ec.mailgun.org/messages",
        auth=("api", "key-cedb9e331a1be78e57582e4e13cac442"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox791822b6aeca4aee8007134fecd331ec.mailgun.org>",
              "to": "Alex <alextrostbtwa@gmail.com>",
              "subject": "Hello Alex",
              "text": "Congratulations Alex, you just sent an email with Mailgun!  You are truly awesome!"})

send_simple_message()