from django.shortcuts import render
import datetime

from brain.models import StudentRoster, Teacher, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, Schedule
from ixl.models import IXLSkillScores, ChallengeAssignment, ChallengeExercise, IXLSkill
from brain.templatetags import brain_extras
from variables import *


def get_current_ixl_challenge(student):
    try:
        ixl_challenge_assignment = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
    except:
        ixl_challenge_assignment = False

    if ixl_challenge_assignment:  # get challenge
        challenge_exercise_list = [] # [(id, description, score), ]
        current_ixl_challenge = ixl_challenge_assignment.challenge
        exercise_list = ChallengeExercise.objects.filter(challenge=current_ixl_challenge) # Get the related exercises
        for exercise in exercise_list:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=exercise.exercise_id).score
            except:
                exercise_score = 0
            exercise_description = IXLSkill.objects.get(skill_id=exercise.exercise_id)
            challenge_exercise_list.append((exercise.exercise_id, exercise_description, exercise_score))
        # Get scores for each challenge
    else:
        challenge_exercise_list = None
        current_ixl_challenge = None
    return challenge_exercise_list



def get_current_amc_challenge(student):
    current_test = brain_extras.amc_number_to_text(brain_extras.current_amc_test(student))
    current_test_name = current_test.name  # Statue of Liberty
    current_test_signifier = current_test.topic  # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
    current_test_topic = current_test.topic.replace(" ",
                                                    "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
    if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
        test_type = 'SUB'
    elif "ADDITION" in current_test_topic:
        test_type = 'ADD'
    elif "MULTIPLICATION" in current_test_topic:
        test_type = 'MUL'
    else:
        test_type = "IMAGE"  # This will be used for clocks, coins, etc.
    combination_set = TESTDICTIONARY[current_test_topic]
    return combination_set, test_type, current_test_name


def school_roster(request, grade="2nd"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    today = datetime.date.today()
    export_list = get_student_info(student_list)


    return render(request, 'parentletter/parent_letter_print.html',
                  {'student_list': student_list, 'export_list': export_list, 'today':today })


def class_roster(request, teacher="Trost"):
    student_list = StudentRoster.objects.filter(current_class__teacher__last_name=teacher)
    today = datetime.date.today()
    export_list = get_student_info(student_list)

    return render(request, 'parentletter/parent_letter_print.html',
                  {'student_list': student_list, 'export_list': export_list, 'today': today})


def get_student_info(student_list):
    export_list = []
    for student in student_list:
        # Get current IXL
        ixl_challenge = get_current_ixl_challenge(student)

        # Get current AMC
        amc_combinations, amc_test_type, amc_test_name = get_current_amc_challenge(student)
        # Check if the AMC is ADD/SUB, otherwise, explain the exercise
        # Add to list
        export_list.append([student, ixl_challenge, amc_combinations, amc_test_type, amc_test_name])
    return export_list


# TODO: IXL Challenges - Add Bonus Exercises to the actual model and create them at the same time
# TODO: This Week Feature - If applicable, the script pulls in paragraphs of current units to discuss what's going on this week
    # TODO: Create Script to pull from Google Doc
# TODO:  Behavior - Pull in applicable data for that specific student and their behavior for the previous week
    # TODO:  Create Script to pull from Google Doc
# TODO:  Homework - Pull in data for if homework was received/incomplete/not received
    # TODO: Create Script to pull from Google Doc

