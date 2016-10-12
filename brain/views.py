from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import random

from .models import StudentRoster, Teacher, CurrentClass, AccountInfo
from amc.models import AMCTestResult
from ixl.models import IXLSkillScores, IXLStats, Challenge, ChallengeAssignment
from libs.functions import nwea_recommended_skills_list, class_skills_list
from brain.models import ReadingStats

GREETINGS = ['Hello', 'Hola', 'Hey there', 'Welcome back', 'Great to see you', "Let's do it", 'Bonjour',
             'You rock', "You've got this", "Work hard, get smart", "Rock it"]

COLORS = ["#51B46D", "#F9845B", "#9e4d83", "#3079AB", "#eb7728", "#E0AB18", "#c38cd4", "#20898c",
          "#39ADD1", "#53BBB4", "#2C9676", "#C25975", "#7D669E", "#F092B0", "#E15258", "#838CC7",
          "#51B46D", "#F9845B", "#9e4d83", "#3079AB", "#eb7728", "#E0AB18", "#c38cd4", "#20898c",
          "#39ADD1", "#53BBB4", "#2C9676", "#C25975", "#7D669E", "#F092B0", "#E15258", "#838CC7",
          ]
ICONS = ['fa-bolt','fa-bicycle', 'fa-graduation-cap',  'fa-paint-brush', 'fa-gift', 'fa-money',
         'fa-lightbulb-o', 'fa-globe', 'fa-paper-plane', 'fa-sun-o', 'fa-pencil', 'fa-paw', 'fa-moon-o',
         'fa-futbol-o', 'fa-gamepad', 'fa-dribbble', 'fa-diamond', 'fa-truck', 'fa-tree', 'fa-heart', 'fa-trophy',
         'fa-star', 'fa-car', 'fa-smile-o', 'fa-rocket', 'fa-motorcycle', 'fa-scissors', 'fa-heart',
         'fa-key', 'fa-shopping-cart', 'fa-magic', 'fa-leaf',
         'fa-space-shuttle', 'fa-cog', 'fa-flag', 'fa-check-square', ]


# def inches_to_points(inches):
#     return inches * 72


# def create_ixl_pdf(request):
#     if 'pdf' in request.POST:
#                 student = StudentRoster.objects.get(last_name="Boyd")
#                 response = HttpResponse(content_type='application/pdf') # Tell the client the response will be an attachment
#                 today = date.today() # Set today's date
#                 filename = 'ixl_list' + today.strftime('%Y-%m-%d') # Set the filename
#                 response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
#                 buffer = BytesIO() # Create BytesIO instance as a temporary file
#                 report = PdfPrint(buffer, 'Letter') # Creates an instance of PDFPrint in report.
#                 pdf = report.recommendation_list(student, 'Recommendation List for {} {}'.format(student.first_name, student.last_name[0])) # args=Weather History/Title
#                 response.write(pdf) # Adds the PDF contents to the response
#                 return response # Returns the response.



# TODO: Teacher List (Sort: Teacher, Incl. Most Recent Grade taught)
# TODO: Grade Roster (Sort: LastName, Incl.: First, Last, Teacher, Grade, Gender, Age)
# TODO: Class List (Sort: Lastname, Incl.: Teacher, Grade: First, Last, Gender, Age)
# TODO: Individual Student Detail (Sort: Custom, Incl.: Teacher, Grade, Gender, Age, All Test Details, Next Skills)


def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(
        current_class__year=year)  # .order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    return render(request, 'brain/year_list.html', {'student_list': student_list, 'year': year,})


def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    teacher_object = Teacher.objects.get(last_name=teacher)
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    recommendation_list = class_skills_list(student_list, "recommended_skill_list")[:10]
    return render(request, 'brain/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher, 'teacher_object': teacher_object,
                                                     'recommendation_list': recommendation_list,})


def student_detail(request, studentid, ):  # Look at a single student's record
    # url: /student/83
    amc_tests = AMCTestResult.objects.all().filter(student_id=studentid)[:5]
    ixl_scores = IXLSkillScores.objects.all().filter(student_id=studentid)
    student = get_object_or_404(StudentRoster, student_id=studentid)
    actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete = nwea_recommended_skills_list(
        student, "all")
    return render(request, 'brain/student_detail.html', {'student': student, 'amc_tests': amc_tests,
                                                         'ixl_scores': ixl_scores,
                                                         "actual_nwea_scores": actual_nwea_scores,
                                                         "estimated_nwea_scores": estimated_nwea_scores,
                                                         "recommended_skill_list": recommended_skill_list,
                                                         "subdomain_percentage_complete": subdomain_percentage_complete})


def index(request):
    return render(request, 'brain/index.html', )


def portal_school(request):  # Portal that lists all the teachers in the school
    class_list = CurrentClass.objects.filter(year="16-17").order_by('teacher', )

    icon_list = ['fa-heart', 'fa-globe', 'fa-rocket', 'fa-car', 'fa-bolt', 'fa-paw', 'fa-graduation-cap',
                 'fa-bicycle', 'fa-paint-brush', 'fa-leaf', 'fa-money',
                 'fa-key', 'fa-lightbulb-o', 'fa-paper-plane', 'fa-pencil', 'fa-moon-o',
                 'fa-futbol-o', 'fa-gamepad', 'fa-dribbble', 'fa-diamond', 'fa-truck', 'fa-tree', 'fa-heart',
                 'fa-trophy',
                 'fa-star', 'fa-smile-o', 'fa-motorcycle', 'fa-check-square', 'fa-scissors',
                 'fa-apple', 'fa-cloud', 'fa-sun-o', 'fa-shopping-cart', 'fa-magic',
                 'fa-space-shuttle', 'fa-gift', 'fa-cog', 'fa-flag']
    return render(request, 'brain/portal_school.html', {'class_list': class_list, 'color_list': COLORS,
                                                        'icon_list': ICONS})


def portal_class(request, teacher="Trost", grade="2nd"):  # Portal that lists all the students in that class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher).order_by('first_name')
    teacher = Teacher.objects.get(last_name=teacher)
    # Sort the student list by their number of IXL minutes spent [:5]
    class_ixl_time_spent = IXLStats.objects.filter(student__current_class__teacher=teacher).order_by('-time_spent')[:5]
    class_ixl_questions_answered = IXLStats.objects.filter(student__current_class__teacher=teacher).order_by(
        '-questions_answered')[:5]
    class_myon_time_spent = ReadingStats.objects.filter(student__current_class__teacher=teacher).order_by('-myon_time_spent')
    for x in range(len(class_myon_time_spent)):
        if not class_myon_time_spent[x].myon_time_spent:
            class_myon_time_spent[x].myon_time_spent = 0
    class_myon_books_read = ReadingStats.objects.filter(student__current_class__teacher=teacher).order_by('-myon_books_finished')
    for x in range(len(class_myon_books_read)):
        if not class_myon_books_read[x].myon_books_finished:
            class_myon_books_read[x].myon_books_finished = 0


    class_myon_time_spent = class_myon_time_spent[:5]
    class_myon_books_read = class_myon_books_read[:5]
    leaderboardteachers = ['Trost','Cyphers', 'Mackinnon', 'DaSilva', "Berrie", "Stein"]
    if teacher.last_name in leaderboardteachers:
        leaderboard_display = True
    else:
        leaderboard_display = False

    return render(request, 'brain/portal_class.html', {'student_list': student_list, 'teacher': teacher, 'grade': grade,
                                                       'color_list': COLORS, 'icon_list': ICONS,
                                                       'class_ixl_time_spent':class_ixl_time_spent, 'leaderboard_display':
                                                           leaderboard_display, 'class_ixl_questions_answered':
                                                        class_ixl_questions_answered, 'class_myon_time_spent':
                                                       class_myon_time_spent, 'class_myon_books_read':class_myon_books_read})


def portal_student(request, teacher, grade,
                   studentid):  # Portal that lists the student's information and provides links to the sites
    student = get_object_or_404(StudentRoster, student_id=studentid)
    try:
        accountinfo = AccountInfo.objects.get(student=student)
    except:
        accountinfo = False
    try:
        readingstats = ReadingStats.objects.get(student=student)
    except:
        readingstats = False
    try:
        ixlstats = IXLStats.objects.get(student=student)
        if ixlstats.last_practiced == -1:
            ixlstats = False
        elif ixlstats.last_practiced == 0:
            ixlstats.last_practiced = "Today"
        elif ixlstats.last_practiced == 1:
            ixlstats.last_practiced = "Yesterday"
        elif ixlstats.last_practiced > 1:
            ixlstats.last_practiced = "{} Days Ago".format(ixlstats.last_practiced)
    except:
        ixlstats = False

    try:
        ixl_challenge = ChallengeAssignment.objects.get(student_id=student, current_challenge=True)
    except:
        ixl_challenge = False
    exercise_scores = []
    if ixl_challenge: #get the 15 challenges and see if they're passed yet. If they're all passed, mark as complete)

        if ixl_challenge.challenge.exercise1:
            try:
                exercise_score = IXLSkillScores.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise1.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise2:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise2.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise3:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise3.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise4:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise4.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise5:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise5.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise6:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise6.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise7:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise7.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise8:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise8.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise9:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise9.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise10:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise10.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise11:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise11.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise12:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise12.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise13:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise13.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise14:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise14.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        if ixl_challenge.challenge.exercise15:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=ixl_challenge.challenge.exercise15.skill_id,)
            except:
                exercise_score = 0
            exercise_scores.append(exercise_score)
        for p in range(len(exercise_scores)):
            if exercise_scores[p] == None:
                exercise_scores[p]=0


    second_and_third_teachers = ['Berrie', 'Stein', 'DaSilva', 'Cyphers', 'Trost', 'Mackinnon']
    if teacher in second_and_third_teachers:
        myon_display = True
    else:
        myon_display = False
    try:
        if readingstats.current_lexile <= 0:
            readingstats.current_lexile = "BR"
    except:
        pass
    try:
        if readingstats.starting_lexile and readingstats.current_lexile and readingstats.goal_lexile:
            lexile_goal_percentage = round((readingstats.current_lexile - readingstats.starting_lexile) / (readingstats.goal_lexile - readingstats.starting_lexile) * 100)
            lexile_goal_percentage = int(lexile_goal_percentage)
        else:
            lexile_goal_percentage = 0
    except:
        lexile_goal_percentage = 0
    lexile_goal_float = str(lexile_goal_percentage)+"%"

    greeting = random.choice(GREETINGS)


    return render(request, 'brain/portal_student.html', {'student': student, 'accountinfo': accountinfo,
                                                         'teacher': teacher, 'grade': grade, 'greeting': greeting,
                                                         'readingstats': readingstats, 'ixlstats': ixlstats,
                                                         'myon_display': myon_display,
                                                         'lexile_goal_percentage': lexile_goal_percentage,
                                                         'lexile_goal_float': lexile_goal_float, 'ixl_challenge':ixl_challenge,
                                                         'exercise_scores':exercise_scores,
                                                         })


def make_groups(request, grade, teacher):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher)
    partner_list = []
    for student in student_list:
        partner_list.append(student.first_name)
    random.shuffle(partner_list)
    final_list = []
    if len(partner_list) % 2 == 0: # Even
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) +" + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break
    else: # Odd
        partnership = partner_list.pop(0) +" + " + partner_list.pop(0)  +" + " + partner_list.pop(0)
        final_list.append(partnership)
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) +" + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break



    return render(request, 'brain/make_groups.html',{'partner_list':final_list, 'color_list':COLORS, 'teacher':teacher})