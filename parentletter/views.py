from django.shortcuts import render
import datetime

from brain.models import StudentRoster, Teacher, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, Schedule
from ixl.models import IXLSkillScores, ChallengeAssignment, ChallengeExercise, IXLSkill
from brain.templatetags import brain_extras

# Create your views here.


ADDITION1 = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0),  (1, 1),
             (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (2, 2)]

ADDITION2 = [(4, 2),  (7, 3),  (3, 3), (5, 2), (6, 4),  (4, 4), (6, 2),  (5, 5),
             (7, 2), (8, 2), (4, 3), (5, 3), (6, 3), (5, 4), (6, 4),]

ADDITION3 = [(6, 5), (7, 4), (8, 3), (9, 2), (6, 6), (7, 5), (8, 4), (9, 3), (7, 6), (8, 5), (9, 4),
             (7, 7), (8, 6), (9, 5), (8, 7), (9, 6), (8, 8), (9, 7), (9, 8), (9, 9)]

ADDITION4 = [(1, 10), (2, 10), (11, 1), (3, 10), (12, 1), (4, 10), (13, 1), (5, 10), (14, 1), (6, 10), (15, 1), (7, 10),
             (16, 1), (8, 10), (17, 1), (9, 10), (18, 1), (10, 10), (19, 1)]

ADDITION5 = [(10, 2), (10, 3), (11, 2), (11, 3), (12, 2), (12, 3), (13, 2), (13, 3), (14, 2), (14, 3), (15, 2), (15, 3),
             (16, 2), (16, 3), (17, 2), (17, 3), (18, 2)]

ADDITION6 = [(11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (12, 4), (12, 5), (12, 6), (12, 7), (11, 9), (13, 4), (13, 5),
             (13, 6), (13, 7), (14, 4), (14, 5), (14, 6), (15, 4), (15, 5), (16, 4)]

SUBTRACTION1 = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (2, 2), (3, 2), (4, 2), (5, 2), (3, 3), (4, 3), (5, 3), (4, 4),
                (5, 4), (5, 5), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), ]

SUBTRACTION2 = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (3, 1), (4, 2), (5, 3),
                (6, 4), (7, 5), (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (6, 1),
                (7, 2), (8, 3), (9, 4), (7, 1), (8, 2), (9, 3), (8, 1), (9, 2), (9, 1)]

SUBTRACTION3 = [(6, 6), (7, 7), (8, 8), (9, 9), (10, 1), (18, 9), (10, 2), (16, 8), (10, 3), (14, 7), (10, 4), (12, 6),
                (10, 5), (10, 6), (10, 7), (9, 6), (10, 8), (8, 6), (9, 7), (10, 9), (7, 6), (8, 7), (9, 8)]

SUBTRACTION4 = [(11, 1), (11, 2), (11, 3), (12, 1), (12, 2), (12, 3), (13, 1), (13, 2), (13, 3), (14, 1), (14, 2),
                (14, 3), (15, 1), (15, 2), (15, 3), (16, 1), (16, 2), (16, 3), (17, 1), (17, 2), (17, 3), (18, 1),
                (18, 2), (18, 3), (19, 1), (19, 2), (19, 3)]

SUBTRACTION5 = [(11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (12, 4), (12, 5), (12, 7), (12, 8), (12, 9),
                (14, 4), (15, 5), (16, 6), (17, 7), (18, 8), (19, 9)]

SUBTRACTION6 = [(13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (14, 5), (14, 6), (14, 8), (14, 9), (15, 4),
                (15, 6), (15, 7), (15, 8), (15, 9), (16, 4), (16, 5), (16, 6), (16, 7), (16, 9), (17, 4), (17, 5),
                (17, 6), (17, 7), (17, 8), (17, 9), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (19, 4), (19, 5),
                (19, 6), (19, 7), (19, 8)]

SUBTRACTION7 = [(13, 7), (13, 8), (13, 9), (14, 8), (14, 9), (15, 7), (15, 8), (15, 9), (16, 7), (16, 9), (17, 7),
                (17, 8), (17, 9), (18, 7), (18, 8), (19, 7), (19, 8)]

TIME = []  # For this the tuple will be an image (time1.png) and the answer (3:45)
MONEY = []
FRACTIONS = []
MULTIPLICATION = []


TESTDICTIONARY = {'ADDITION1': ADDITION1, 'ADDITION2': ADDITION2, 'ADDITION3': ADDITION3, 'ADDITION4': ADDITION4,
                  'ADDITION5': ADDITION5, 'ADDITION6': ADDITION6, 'SUBTRACTION1': SUBTRACTION1,
                  'SUBTRACTION2': SUBTRACTION2, 'SUBTRACTION3': SUBTRACTION3, 'SUBTRACTION4': SUBTRACTION4,
                  'SUBTRACTION5': SUBTRACTION5,
                  'SUBTRACTION6': SUBTRACTION6, 'SUBTRACTION7': SUBTRACTION7, 'TIME':TIME, 'MONEY':MONEY,
                  'FRACTIONS':FRACTIONS, 'MULTIPLICATION':MULTIPLICATION}

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
    else:
        test_type = "IMAGE"  # This will be used for clocks, coins, etc.
    combination_set = TESTDICTIONARY[current_test_topic]
    return combination_set, test_type, current_test_name




def school_roster(request, grade="2nd"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    today = datetime.date.today()
    # Get student list
    export_list = []
    for student in student_list:
        # Get current IXL
        ixl_challenge = get_current_ixl_challenge(student)

        # Get current AMC
        amc_combinations, amc_test_type, amc_test_name = get_current_amc_challenge(student)
        # Check if the AMC is ADD/SUB, otherwise, explain the exercise
        # Add to list
        export_list.append([student, ixl_challenge, amc_combinations, amc_test_type, amc_test_name])


    return render(request, 'parentletter/parent_letter_print.html',
                  {'student_list': student_list, 'export_list': export_list, 'today':today })



def break_challenge(request, grade="2nd"):
    pass