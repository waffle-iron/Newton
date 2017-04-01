import datetime
import random

from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from . import forms
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras
from amc.models import AMCTestResult, AMCTest

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

TIME = [('clock-01-40', '1:40'),('clock-02-30', '2:30'),('clock-03-35', '3:35'),('clock-03-45', '3:45'),('clock-05-10', '5:10'),
        ('clock-05-45', '5:45'),
        ('clock-06-15', '6:15'),('clock-07-30', '7:30'),('clock-07-40', '7:40'),('clock-08-25', '8:25'),('clock-09-35', '9:35'),
        ('clock-10-40', '10:40'),
        ('clock-11-20', '11:20'),('clock-12-50', '12:50'),]
MONEY = []
FRACTIONS = []

TESTDICTIONARY = {'ADDITION1': ADDITION1, 'ADDITION2': ADDITION2, 'ADDITION3': ADDITION3, 'ADDITION4': ADDITION4,
                  'ADDITION5': ADDITION5, 'ADDITION6': ADDITION6, 'SUBTRACTION1': SUBTRACTION1,
                  'SUBTRACTION2': SUBTRACTION2, 'SUBTRACTION3': SUBTRACTION3, 'SUBTRACTION4': SUBTRACTION4,
                  'SUBTRACTION5': SUBTRACTION5,
                  'SUBTRACTION6': SUBTRACTION6, 'SUBTRACTION7': SUBTRACTION7, 'TIME':TIME,'MONEY':MONEY,}


def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(
        current_class__year=year)  # .order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    teacher_list = CurrentClass.objects.filter(year=year)
    return render(request, 'amc/index.html',
                  {'student_list': student_list, 'year': year, 'teacher_list': teacher_list,})


def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    amc_tests = AMCTestResult.objects.all()

    return render(request, 'amc/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                   'teacher': teacher, 'amc_tests': amc_tests})

# This one is for the Challenge Sheets - Flash Cards
def get_student_and_test_list_for_challenges(student_list):
    student_and_test_list = []
    for student in student_list:
        if student.first_name == "Stephen":
             continue
        elif brain_extras.amc_badges_earned(student) ==10:
            continue
        current_test_number = brain_extras.current_amc_test(
            student)  # Run script to figure out the current test for student
        current_test = AMCTest.objects.get(test_number=current_test_number)  # Get the current test
        current_test_name = current_test.name # Statue of Liberty
        current_test_signifier = current_test.topic # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
        current_test_topic = current_test.topic.replace(" ",
                                                        "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
        if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
            test_type = 'SUB'
        elif "ADDITION" in current_test_topic:
            test_type = 'ADD'
        else:
            test_type = "IMAGE"  # This will be used for clocks, coins, etc.

        first_name = student.first_name  # Split these for ease of use down the line
        last_name = student.last_name
        # Now put all the information into the tuple and append the tuple to the list
        combinationset = TESTDICTIONARY[current_test_topic]
        # finallist order will go [(1,2), (1,3), (1,4)..., (1,9), 3, 4, 5... 10], [(2,2)...4]
        tempcombolist = []
        tempanswerlist = []
        finallist = []
        for combination in combinationset:
            # Get the first combination and add it to a short combo list
            var1, var2 = combination
            tempcombolist.append((var1, var2))
            # Add those two numbers together and add that to a short answer list
            if test_type == 'ADD':
                tempanswerlist.append(var1+var2)
            elif test_type == 'SUB':
                tempanswerlist.append(var1 - var2)
            elif test_type == 'IMAGE':
                tempanswerlist.append(var2)
            # Repeat until you have 10 items in both lists, then append those lists together into one list.
            if len(tempcombolist) == 10:
            # Then put that list as a new item at the end of the big list.
                tempanswerlist[0], tempanswerlist[1] = tempanswerlist[1], tempanswerlist[0]
                tempanswerlist[2], tempanswerlist[3] = tempanswerlist[3], tempanswerlist[2]
                tempanswerlist[4], tempanswerlist[5] = tempanswerlist[5], tempanswerlist[4]
                tempanswerlist[6], tempanswerlist[7] = tempanswerlist[7], tempanswerlist[6]
                tempanswerlist[8], tempanswerlist[9] = tempanswerlist[9], tempanswerlist[8]
                j = tempcombolist + tempanswerlist
                finallist.append(j)
                tempcombolist = []
                tempanswerlist = []
        if len(tempcombolist):
            while len(tempcombolist) != 10:
                tempcombolist.append('None')
                tempanswerlist.append('None')
            tempanswerlist[0], tempanswerlist[1] = tempanswerlist[1], tempanswerlist[0]
            tempanswerlist[2], tempanswerlist[3] = tempanswerlist[3], tempanswerlist[2]
            tempanswerlist[4], tempanswerlist[5] = tempanswerlist[5], tempanswerlist[4]
            tempanswerlist[6], tempanswerlist[7] = tempanswerlist[7], tempanswerlist[6]
            tempanswerlist[8], tempanswerlist[9] = tempanswerlist[9], tempanswerlist[8]
            j = tempcombolist + tempanswerlist
            finallist.append(j)
            tempcombolist = []
            tempanswerlist = []

        student_list_entry = (first_name, last_name, current_test_name, test_type,
                              finallist, current_test_signifier)

        student_and_test_list.append(student_list_entry)
    return student_and_test_list

# This one is for the Test Sheets
def get_student_and_test_list_for_tests(student_list):
    student_and_test_list = []
    for student in student_list:
        if student.first_name == "Stephen":
            continue
        elif brain_extras.amc_badges_earned(student) ==10:
            continue
        current_test_number = brain_extras.current_amc_test(
            student)  # Run script to figure out the current test for student
        current_test = AMCTest.objects.get(test_number=current_test_number)  # Get the current test
        current_test_name = current_test.name
        current_test_signifier = current_test.topic # Keeps a string for "Addition 1" or "Subtraction 5" or "Fractions"
        current_test_topic = current_test.topic.replace(" ",
                                                        "").upper()  # Get the Topic (Addition 3) and turn it into ADDITION3
        if 'SUBTRACTION' in current_test_topic:  # This is for the Template so it knows if we're adding or subtracting
            test_type = 'SUB'
        elif "ADDITION" in current_test_topic:
            test_type = 'ADD'
        else:
            test_type = "IMAGE"  # This will be used for clocks, coins, etc.

        first_name = student.first_name  # Split these for ease of use down the line
        last_name = student.last_name
        # Randomize Combinations and pull first 20 from list. If you run out of combos, loop around.
        problem_list = TESTDICTIONARY[current_test_topic]
        random.shuffle(problem_list)
        test_list = []
        for i in problem_list:
            test_list.append(i)
        if test_type == 'IMAGE':
            test_list = test_list[:9]
        else:
            test_list=test_list[:20]
            if len(test_list) < 20:
                n = 0
                while len(test_list) < 20:
                    test_list.append(test_list[n])
                    n += 1
        # Now put all the information into the tuple and append the tuple to the list
        student_list_entry = (first_name, last_name, current_test_name, test_type,
                              test_list, current_test_signifier)
        student_and_test_list.append(student_list_entry)
    return student_and_test_list


def print_challenge_sheets_class(request, year="16-17", grade="2nd", teacher="Trost"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    student_and_test_list = get_student_and_test_list_for_challenges(student_list)

    return render(request, 'amc/amc_card_print.html',
                  {'year': year, 'grade': grade, 'teacher': teacher, 'student_and_test_list': student_and_test_list})


def print_challenge_sheets_grade(request, year="16-17", grade="2nd"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    student_and_test_list = get_student_and_test_list_for_challenges(student_list)
    return render(request, 'amc/amc_card_print.html',
                  {'year': year, 'grade': grade, 'student_and_test_list': student_and_test_list,})


def print_test_sheets_class(request, year="16-17", grade="2nd", teacher="Trost"):

    # Get list of students in this class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    # Use list of students and the current test they're taking.
    student_and_test_list=get_student_and_test_list_for_tests(student_list)
    random_list = [0,1,2,3]



    return render(request, 'amc/amc_test_print.html',
                  {'year': year, 'grade': grade, 'teacher': teacher, 'student_and_test_list': student_and_test_list, 'random_list':random_list,})


def print_test_sheets_grade(request, year="16-17", grade="2nd", teacher="Trost"):
    # Get list of students in this grade
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year)
    # Use list of students and the current test they're taking.
    student_and_test_list=get_student_and_test_list_for_tests(student_list)
    random_list = [0,1,2,3]
    return render(request, 'amc/amc_test_print.html',
                  {'year': year, 'grade': grade, 'teacher': teacher, 'student_and_test_list': student_and_test_list,
                   'random_list':random_list})



@login_required
def input_amc_scores(request, year="16-17", grade="2nd", teacher="Trost"):
    if request.method == 'POST':
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=0)
        formset = TestListFormSet(request.POST)
        has_errors = False
        for form in formset:
            # Seems like it should be possible to have the form know the instance it was created from, and update
            # that rather than go through this manual process
            if form.is_valid():
                form.save()
            else:
                existing_results = AMCTestResult.objects.filter(student=form.instance.student,
                                                                date_tested=form.instance.date_tested)
                if form.instance.score and existing_results.count():
                    instance = existing_results.first()
                    instance.score = form.instance.score
                    instance.save()
                else:
                    has_errors = True
                    print(form.errors)
        messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded!")
        if not has_errors:
            url = reverse('amc:classlist', kwargs={'year': year, 'grade': grade, 'teacher': teacher})
            return HttpResponseRedirect(url)
    else:
        student_list = StudentRoster.objects.filter(current_class__grade=grade) \
            .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)

        form_count = student_list.count()
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=form_count)
        formset = TestListFormSet()
        # Would be nice to create forms from the instances rather than manually set initial, but that did not seem
        # to work correctly
        for i in range(form_count):
            today = datetime.date.today()
            existing_results = AMCTestResult.objects.filter(student=student_list[i], date_tested=today)
            initial_test = brain_extras.current_amc_test(student_list[i])
            if existing_results.count():
                instance = existing_results.first()
                formset.forms[i].instance = instance
                initial_student = instance.student
                initial_score = instance.score
            else:
                initial_student = student_list[i]
                initial_score = None
            formset.forms[i].fields['student'].initial = initial_student
            formset.forms[i].fields['test'].initial = initial_test
            formset.forms[i].fields['score'].initial = initial_score


    return render(request, 'amc/input_amc_scores_form.html', {
        'formset': formset,
        'teacher': teacher,
        'grade': grade,
        'year': year,
    })


def amc_index(request):
    return HttpResponse("You're at the AMC index!")
